"""
CV Analyzer - основной модуль для анализа резюме с помощью Mistral AI
"""
import os
import json
import requests
import time
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from config import MISTRAL_API_URL, MISTRAL_MODEL, get_mistral_api_key
from .prompts import (
    ANALYZE_CV_PROMPT, 
    ANALYZE_CV_WITH_JOB_DESCRIPTION_PROMPT,
    SIMPLE_CV_ANALYSIS_PROMPT,
    CANDIDATE_COMPARISON_MATRIX_PROMPT,
    COMBINE_AND_ANALYZE_CANDIDATES_PROMPT,
    WHICH_CANDIDATE_TO_HIRE_PROMPT
)

# Загружаем .env файл
load_dotenv()

class CVAnalyzer:
    """
    Анализатор резюме с использованием Mistral AI
    """
    
    def __init__(self):
        """Инициализация анализатора"""
        self.api_url = MISTRAL_API_URL
        self.model = MISTRAL_MODEL
        self.api_key = get_mistral_api_key()
    
    def _make_mistral_request(self, prompt: str, max_retries: int = 3) -> str:
        """
        Выполняет запрос к Mistral AI API с повторными попытками
        """
        import logging
        logger = logging.getLogger(__name__)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.1
        }
        
        for attempt in range(max_retries):
            try:
                logger.info(f"[MISTRAL_API] Making request to {self.api_url} (attempt {attempt + 1})")
                response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
                response.raise_for_status()
                
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    logger.info(f"[MISTRAL_API] Successfully received response (length: {len(content)})")
                    
                    # Clean up the response - remove markdown code blocks if present
                    cleaned_content = self._clean_ai_response(content)
                    
                    return cleaned_content
                else:
                    logger.error(f"[MISTRAL_API] Unexpected response format: {result}")
                    raise ValueError("Unexpected response format")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"[MISTRAL_API] Request failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
        raise Exception("All retry attempts failed")

    def _clean_ai_response(self, response: str) -> str:
        """
        Очищает ответ AI от markdown блоков и лишнего текста
        """
        # Remove markdown code blocks
        if "```json" in response:
            # Extract JSON from markdown code block
            start_idx = response.find("```json")
            if start_idx != -1:
                start_idx = response.find("\n", start_idx) + 1
                end_idx = response.find("```", start_idx)
                if end_idx != -1:
                    return response[start_idx:end_idx].strip()
        
        # Remove other markdown code blocks
        if "```" in response:
            # Extract content between code blocks
            start_idx = response.find("```")
            if start_idx != -1:
                start_idx = response.find("\n", start_idx) + 1
                end_idx = response.find("```", start_idx)
                if end_idx != -1:
                    return response[start_idx:end_idx].strip()
        
        # Remove common prefixes
        prefixes_to_remove = [
            "Here is the JSON response analyzing the CV against the job requirements:",
            "Here is the analysis result:",
            "Here is the comparison matrix:",
            "Here is the hiring recommendation:",
            "Here is the summary:"
        ]
        
        cleaned_response = response.strip()
        for prefix in prefixes_to_remove:
            if cleaned_response.startswith(prefix):
                cleaned_response = cleaned_response[len(prefix):].strip()
        
        return cleaned_response

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Извлекает текст из PDF файла
        """
        try:
            import PyPDF2
            import io
            
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_bytes: bytes) -> str:
        """
        Извлекает текст из DOCX файла
        """
        try:
            import docx
            import io
            
            docx_file = io.BytesIO(docx_bytes)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""

    def analyze_cv_detailed(self, cv_text: str, job_description: str = "") -> Dict[str, Any]:
        """
        Детальный анализ CV с полной структурой achievers_rating
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            if job_description:
                prompt = ANALYZE_CV_WITH_JOB_DESCRIPTION_PROMPT.format(
                    cv_text=cv_text,
                    job_description=job_description
                )
            else:
                prompt = ANALYZE_CV_PROMPT.format(
                    cv_text=cv_text,
                    requirements_text="General software development position"
                )
            
            logger.info(f"[MISTRAL] About to call Mistral API with prompt length: {len(prompt)}")
            response = self._make_mistral_request(prompt)
            
            # Try to parse as JSON first
            try:
                result = json.loads(response.strip())
                logger.info(f"[MISTRAL] Successfully parsed detailed analysis JSON")
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"[MISTRAL] Failed to parse JSON response: {e}")
                logger.warning(f"[MISTRAL] Response preview: {response[:500]}")
                
                # Fallback to simple analysis
                return self.analyze_cv_simple(cv_text, job_description)
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error in detailed analysis: {e}")
            # Fallback to simple analysis
            return self.analyze_cv_simple(cv_text, job_description)

    def analyze_cv_simple(self, cv_text: str, job_description: str = "") -> Dict[str, Any]:
        """
        Простой анализ CV с базовыми оценками
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            prompt = SIMPLE_CV_ANALYSIS_PROMPT.format(cv_text=cv_text)
            
            logger.info(f"[MISTRAL] About to call Mistral API with simple prompt length: {len(prompt)}")
            response = self._make_mistral_request(prompt)
            
            # Try to parse as JSON first
            try:
                result = json.loads(response.strip())
                logger.info(f"[MISTRAL] Successfully parsed simple analysis JSON")
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"[MISTRAL] Failed to parse JSON response: {e}")
                logger.warning(f"[MISTRAL] Response preview: {response[:500]}")
                
                # Fallback to basic response
                return {
                    "full_name": "Unknown",
                    "summary": "Analysis failed",
                    "overall_score": 50,
                    "skills_score": 50,
                    "experience_score": 50,
                    "education_score": 50,
                    "match_score": 50,
                    "strengths": ["Analysis could not be completed"],
                    "weaknesses": ["Technical issue with AI analysis"],
                    "recommendations": ["Please try again or contact support"]
                }
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error in simple analysis: {e}")
            return {
                "full_name": "Unknown",
                "summary": "Analysis failed due to technical error",
                "overall_score": 0,
                "skills_score": 0,
                "experience_score": 0,
                "education_score": 0,
                "match_score": 0,
                "strengths": [],
                "weaknesses": ["Technical error prevented analysis"],
                "recommendations": ["Please check your API configuration"]
            }

    def analyze_cv_with_score(self, cv_text: str, job_description: str = "") -> Dict[str, Any]:
        """
        Анализ CV с оценками от 0 до 100 (совместимость с существующим API)
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Сначала пробуем детальный анализ
            detailed_result = self.analyze_cv_detailed(cv_text, job_description)
            
            # Если есть achievers_rating, конвертируем в формат оценок
            if "achievers_rating" in detailed_result:
                achievers = detailed_result["achievers_rating"]
                overall_score = achievers.get("overall_score", 0)
                
                # Конвертируем achievers_rating в формат оценок 0-100
                return {
                    "full_name": detailed_result.get("experience_summary", {}).get("full_name", "Unknown"),
                    "summary": detailed_result.get("experience_summary", {}).get("summary", ""),
                    "years_of_experience": detailed_result.get("experience_summary", {}).get("years_of_experience", ""),
                    "key_skills": detailed_result.get("experience_summary", {}).get("skills_1_plus_years", ""),
                    "technologies": detailed_result.get("experience_summary", {}).get("technologies", ""),
                    "education": f"{detailed_result.get('experience_summary', {}).get('education_degree', '')} - {detailed_result.get('experience_summary', {}).get('education_major', '')}",
                    "certifications": detailed_result.get("experience_summary", {}).get("certifications", ""),
                    "overall_score": min(overall_score * 5, 100),  # Масштабируем до 100
                    "skills_score": min(achievers.get("skills", {}).get("score", 0) * 10, 100),
                    "experience_score": min(achievers.get("experience_bonus", {}).get("score", 0) * 20, 100),
                    "education_score": 75,  # Базовая оценка для образования
                    "match_score": int(detailed_result.get("overall_assessment", {}).get("match_score", 0.5) * 100),
                    "strengths": detailed_result.get("overall_assessment", {}).get("strengths", []),
                    "weaknesses": detailed_result.get("overall_assessment", {}).get("weaknesses", []),
                    "recommendations": [rec.get("suggestion", "") for rec in detailed_result.get("recommendations", [])],
                    "availability": "Available",
                    "score_breakdown": {
                        "skills_quality": min(achievers.get("skills", {}).get("score", 0) * 10, 100),
                        "experience_depth": min(achievers.get("experience_bonus", {}).get("score", 0) * 20, 100),
                        "education_quality": 75,
                        "overall_impression": min(overall_score * 5, 100)
                    },
                    # Добавляем детальную структуру для совместимости
                    "achievers_rating": achievers,
                    "experience_summary": detailed_result.get("experience_summary", {}),
                    "requirements_analysis": detailed_result.get("requirements_analysis", {}),
                    "overall_assessment": detailed_result.get("overall_assessment", {})
                }
            else:
                # Если нет achievers_rating, используем простой анализ
                return self.analyze_cv_simple(cv_text, job_description)
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error in analyze_cv_with_score: {e}")
            return self.analyze_cv_simple(cv_text, job_description)

    def generate_comparison_matrix(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Генерирует матрицу сравнения кандидатов
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Подготавливаем данные для сравнения
            candidates_json = json.dumps(candidates_data, indent=2, ensure_ascii=False)
            
            prompt = CANDIDATE_COMPARISON_MATRIX_PROMPT.format(
                candidates_data=candidates_json
            )
            
            logger.info(f"[MISTRAL] Generating comparison matrix for {len(candidates_data)} candidates")
            response = self._make_mistral_request(prompt)
            
            # Парсим JSON ответ
            try:
                result = json.loads(response.strip())
                logger.info(f"[MISTRAL] Successfully generated comparison matrix")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"[MISTRAL] Failed to parse comparison matrix JSON: {e}")
                return {
                    "error": "Failed to generate comparison matrix",
                    "candidates_data": candidates_data
                }
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error generating comparison matrix: {e}")
            return {
                "error": f"Error generating comparison matrix: {str(e)}",
                "candidates_data": candidates_data
            }

    def analyze_multiple_candidates(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Анализирует несколько кандидатов вместе
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Подготавливаем данные для анализа
            candidates_json = json.dumps(candidates_data, indent=2, ensure_ascii=False)
            
            prompt = COMBINE_AND_ANALYZE_CANDIDATES_PROMPT.format(
                candidates_data=candidates_json
            )
            
            logger.info(f"[MISTRAL] Analyzing {len(candidates_data)} candidates together")
            response = self._make_mistral_request(prompt)
            
            # Парсим JSON ответ
            try:
                result = json.loads(response.strip())
                logger.info(f"[MISTRAL] Successfully analyzed multiple candidates")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"[MISTRAL] Failed to parse multiple candidates analysis JSON: {e}")
                return {
                    "error": "Failed to analyze multiple candidates",
                    "candidates_data": candidates_data
                }
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error analyzing multiple candidates: {e}")
            return {
                "error": f"Error analyzing multiple candidates: {str(e)}",
                "candidates_data": candidates_data
            }

    def get_hiring_recommendations(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Получает рекомендации по найму для кандидатов
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Подготавливаем данные для анализа
            candidates_json = json.dumps(candidates_data, indent=2, ensure_ascii=False)
            
            prompt = WHICH_CANDIDATE_TO_HIRE_PROMPT.format(
                candidates_data=candidates_json
            )
            
            logger.info(f"[MISTRAL] Getting hiring recommendations for {len(candidates_data)} candidates")
            response = self._make_mistral_request(prompt)
            
            # Парсим JSON ответ
            try:
                result = json.loads(response.strip())
                logger.info(f"[MISTRAL] Successfully generated hiring recommendations")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"[MISTRAL] Failed to parse hiring recommendations JSON: {e}")
                return {
                    "error": "Failed to generate hiring recommendations",
                    "candidates_data": candidates_data
                }
                
        except Exception as e:
            logger.error(f"[MISTRAL] Error getting hiring recommendations: {e}")
            return {
                "error": f"Error getting hiring recommendations: {str(e)}",
                "candidates_data": candidates_data
            } 