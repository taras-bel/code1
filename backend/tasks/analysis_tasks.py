"""
Background tasks for CV analysis using Celery
"""
import os
import logging
from celery import Celery
from supabase import create_client, Client
from cv_analysis.cv_analyzer import CVAnalyzer
from config import BUCKET_NAME, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импортируем Celery app из celery_app.py
from tasks.celery_app import celery_app

# Supabase клиент
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

@celery_app.task(bind=True, max_retries=3)
def analyze_cv_background(self, analysis_id: str):
    """
    Фоновая задача для анализа CV с оценками от 0 до 100
    """
    try:
        logger.info(f"Starting CV analysis for analysis_id: {analysis_id}")
        
        # Инициализируем анализатор в самом начале
        analyzer = CVAnalyzer()
        
        # Получаем анализ из базы данных
        resp = supabase.table("analyses").select("*").eq("id", analysis_id).single().execute()
        if not resp.data:
            raise ValueError(f"Analysis not found: {analysis_id}")
        
        analysis = resp.data
        user_id = analysis["user_id"]
        job_description = analysis.get("job_description", "")
        job_description_text = ""

        # Если job_description выглядит как путь к PDF-файлу
        if isinstance(job_description, str) and job_description.lower().endswith(".pdf"):
            try:
                file_bytes = supabase.storage.from_(BUCKET_NAME).download(job_description)
                temp_analyzer = CVAnalyzer()
                job_description_text = temp_analyzer.extract_text_from_pdf(file_bytes)
                logger.info(f"[ANALYSIS] Extracted job description from PDF: {job_description_text[:200]}")
                
                # Check if extraction failed (raw PDF content)
                if not job_description_text.strip() or job_description_text.startswith('%PDF'):
                    logger.warning("[ANALYSIS] Job description PDF extraction failed, using generic description")
                    job_description_text = "Software development position requiring technical skills and experience"
                    
            except Exception as e:
                logger.error(f"Error extracting text from job_description PDF: {e}")
                job_description_text = "Software development position requiring technical skills and experience"
        else:
            job_description_text = job_description

        # Обновляем статус на "processing"
        supabase.table("analyses").update({"status": "processing"}).eq("id", analysis_id).execute()
        
        # Получаем все файлы этого анализа
        files_resp = supabase.table("uploaded_files").select("*").eq("analysis_id", analysis_id).execute()
        files = files_resp.data or []
        logger.info(f"[ANALYSIS] Found {len(files)} files for analysis_id={analysis_id}: {[f['filename'] for f in files]}")
        
        if not files:
            raise ValueError("No files uploaded for this analysis")
            
        # Скачиваем и извлекаем текст из всех файлов
        texts = []
        for f in files:
            try:
                # Скачиваем файл из Supabase Storage
                file_bytes = supabase.storage.from_(BUCKET_NAME).download(f["file_path"])
                file_type = f["file_type"].lower()
                
                # Извлекаем текст в зависимости от типа файла
                if file_type == "pdf":
                    text = analyzer.extract_text_from_pdf(file_bytes)
                elif file_type == "docx":
                    text = analyzer.extract_text_from_docx(file_bytes)
                elif file_type == "doc":
                    text = "[DOC file: manual review required]"
                else:
                    text = f"[Unsupported file type: {file_type}]"
                
                logger.info(f"[ANALYSIS] File: {f['filename']} | First 200 chars: {text[:200]}")
                texts.append(f"--- {f['filename']} ---\n{text}")
                logger.info(f"Successfully extracted text from {f['filename']}")
                
            except Exception as e:
                logger.error(f"Error processing file {f['filename']}: {e}")
                texts.append(f"--- {f['filename']} ---\n[Error extracting text: {e}]")
        
        # Объединяем все тексты
        all_text = "\n\n".join(texts)
        
        logger.info(f"[ANALYSIS] Job description text (first 200 chars): {job_description_text[:200]}")
        logger.info(f"[ANALYSIS] All CV text (first 200 chars): {all_text[:200]}")
        
        # If job description extraction failed, use a generic one
        if not job_description_text.strip():
            logger.warning("[ANALYSIS] Job description extraction failed, using generic description")
            job_description_text = "Software development position requiring technical skills and experience"
        
        if not all_text.strip():
            error_msg = "No text extracted from uploaded files. PDF/DOCX may be empty or not parsable."
            logger.error(error_msg)
            supabase.table("analyses").update({
                "status": "failed",
                "error_message": error_msg
            }).eq("id", analysis_id).execute()
            return {"status": "failed", "analysis_id": analysis_id, "error": error_msg}
        
        # Выполняем AI-анализ с оценками
        logger.info("Starting AI analysis with scoring...")
        logger.info(f"[TASK] About to call analyze_cv_with_score with text length: {len(all_text)}")
        logger.info(f"[TASK] Job description length: {len(job_description_text)}")
        results = analyzer.analyze_cv_with_score(all_text, job_description_text)
        logger.info(f"[TASK] analyze_cv_with_score completed, results keys: {list(results.keys()) if results else 'None'}")
        
        # Добавляем метаданные анализа
        results["analysis_metadata"] = {
            "total_files": len(files),
            "file_types": list(set([f["file_type"] for f in files])),
                "analysis_id": analysis_id,
            "job_description_provided": bool(job_description_text.strip())
        }
        
        # Сохраняем результат в базу данных
        logger.info(f"[ANALYSIS] Saving results to database for analysis_id: {analysis_id}")
        logger.info(f"[ANALYSIS] Results keys: {list(results.keys())}")
        
        try:
            update_data = {
                "results": results,
                "status": "completed",
                "processing_time": 0  # Можно добавить реальное время обработки
            }
            logger.info(f"[ANALYSIS] Update data: {update_data}")
            
            response = supabase.table("analyses").update(update_data).eq("id", analysis_id).execute()
            logger.info(f"[ANALYSIS] Database update response: {response}")
            
            if not response.data:
                logger.error(f"[ANALYSIS] No data returned from database update")
                raise Exception("Database update returned no data")
                
        except Exception as db_error:
            logger.error(f"[ANALYSIS] Database update error: {db_error}")
            # Try without processing_time if it fails
            try:
                update_data = {
                    "results": results,
                    "status": "completed"
                }
                logger.info(f"[ANALYSIS] Retry update data: {update_data}")
                
                response = supabase.table("analyses").update(update_data).eq("id", analysis_id).execute()
                logger.info(f"[ANALYSIS] Retry database update response: {response}")
                
                if not response.data:
                    logger.error(f"[ANALYSIS] Retry database update returned no data")
                    raise Exception("Retry database update returned no data")
                    
            except Exception as retry_error:
                logger.error(f"[ANALYSIS] Retry database update also failed: {retry_error}")
                raise
        
        logger.info(f"[ANALYSIS] CV analysis completed successfully for analysis_id: {analysis_id}")
        logger.info(f"[ANALYSIS] About to return result: {{'status': 'completed', 'analysis_id': '{analysis_id}'}}")
        return {"status": "completed", "analysis_id": analysis_id}
        
    except Exception as e:
        logger.error(f"Error in CV analysis for {analysis_id}: {e}")
        
        # Обновляем статус на "failed" и сохраняем ошибку
        try:
            supabase.table("analyses").update({
                "status": "failed",
                "error_message": str(e)
            }).eq("id", analysis_id).execute()
        except Exception as update_error:
            logger.error(f"Failed to update analysis status: {update_error}")
        
        # Повторная попытка, если это не последняя
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying analysis for {analysis_id} (attempt {self.request.retries + 1})")
            raise self.retry(countdown=60 * (self.request.retries + 1))  # Экспоненциальная задержка
        else:
            logger.error(f"Max retries reached for analysis {analysis_id}")
            raise

@celery_app.task(bind=True, max_retries=3)
def compare_candidates_background(self, analysis_id: str, candidates_data: list, job_description: str):
    """
    Фоновая задача для сравнения кандидатов с оценками от 0 до 100
    """
    try:
        logger.info(f"Starting candidate comparison for analysis_id: {analysis_id}")
        
        # Инициализируем анализатор
        analyzer = CVAnalyzer()
        
        # Выполняем сравнение кандидатов
        comparison_results = analyzer.compare_candidates(candidates_data, job_description)
        
        # Добавляем метаданные сравнения
        comparison_results["comparison_metadata"] = {
            "analysis_id": analysis_id,
            "total_candidates": len(candidates_data),
            "job_description_provided": bool(job_description.strip())
        }
        
        # Сохраняем результат в базу данных
        supabase.table("analyses").update({
            "results": comparison_results,
            "status": "completed"
        }).eq("id", analysis_id).execute()
            
        logger.info(f"Candidate comparison completed successfully for analysis_id: {analysis_id}")
        return {"status": "completed", "analysis_id": analysis_id}
            
    except Exception as e:
        logger.error(f"Error in candidate comparison for {analysis_id}: {e}")
        
        # Обновляем статус на "failed" и сохраняем ошибку
        try:
            supabase.table("analyses").update({
                "status": "failed",
                "error_message": str(e)
            }).eq("id", analysis_id).execute()
        except Exception as update_error:
            logger.error(f"Failed to update analysis status: {update_error}")
        
        # Повторная попытка, если это не последняя
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying comparison for {analysis_id} (attempt {self.request.retries + 1})")
            raise self.retry(countdown=60 * (self.request.retries + 1))
        else:
            logger.error(f"Max retries reached for comparison {analysis_id}")
            raise 