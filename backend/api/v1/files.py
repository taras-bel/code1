"""
File upload and management endpoints for API v1
"""
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from datetime import datetime
import mimetypes
from supabase import create_client, Client

# from database.connection import get_db  # Commented out - not needed with Supabase SDK
from database.models import UploadedFile, Analysis, User
from security.auth import decode_jwt_token
# from cv_analysis.cv_analyzer import extract_text_from_file
from config import BUCKET_NAME, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

router = APIRouter()

# Security
bearer_scheme = HTTPBearer()

# Supabase client
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Pydantic models
class FileResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int
    page: int
    per_page: int

def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )

@router.post("/upload")
async def upload_files(
    file: List[UploadFile] = File(...),
    analysis_id: str = Form(...),
    credentials=Depends(bearer_scheme)
):
    """
    Upload a single CV/JD file to Supabase Storage and register in uploaded_files table.
    Only one candidate file per request is allowed (except JD).
    """
    user_id = decode_jwt_token(credentials.credentials)
    results = []

    # Проверка: только 1 файл-кандидат за раз (JD можно отдельно)
    candidate_files = [f for f in file if f.filename and not f.filename.lower().startswith('job_description')]
    jd_files = [f for f in file if f.filename and f.filename.lower().startswith('job_description')]
    if len(candidate_files) > 1:
        raise HTTPException(status_code=400, detail="Загружайте только один файл-кандидата за раз.")

    # Проверка: analysis_id существует и принадлежит пользователю
    analysis = supabase.table("analyses").select("*").eq("id", analysis_id).single().execute().data
    if not analysis or analysis["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Недопустимый analysis_id или нет доступа.")

    # Проверка: не смешивать JD и кандидатов в одном analysis
    existing_files = supabase.table("uploaded_files").select("filename").eq("analysis_id", analysis_id).execute().data or []
    has_jd = any(f["filename"].lower().startswith("job_description") for f in existing_files)
    has_candidate = any(not f["filename"].lower().startswith("job_description") for f in existing_files)
    if jd_files and has_candidate:
        raise HTTPException(status_code=400, detail="Нельзя загружать JD в analysis, где уже есть кандидатский файл. Для JD создайте отдельный analysis.")
    if candidate_files and has_jd:
        raise HTTPException(status_code=400, detail="Нельзя загружать кандидата в analysis, где уже есть JD-файл. Для кандидата создайте отдельный analysis.")

    for f in file:
        try:
            validate_file(f)
            content = await f.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large: {f.filename} ({len(content) // (1024*1024)}MB)"
                )
            mime_type = f.content_type or (mimetypes.guess_type(f.filename or "")[0] or "application/octet-stream")
            storage_path = f"{user_id}/{analysis_id}/{f.filename}"
            res = supabase.storage.from_(BUCKET_NAME).upload(
                storage_path,
                content,
                {"content-type": mime_type}
            )
            if not res or getattr(res, 'error', None):
                error_msg = getattr(res, 'error', 'Unknown error') if res else 'Unknown error'
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload {f.filename} to storage: {error_msg}"
                )
            file_record = {
                "analysis_id": analysis_id,
                "filename": f.filename,
                "file_path": storage_path,
                "file_type": os.path.splitext(f.filename or "")[1][1:],
                "file_size": len(content),
                "mime_type": mime_type,
                "user_id": user_id
            }
            dbres = supabase.table("uploaded_files").insert(file_record).execute()
            if not dbres.data or not dbres.data[0].get("id"):
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to register {f.filename} in database"
                )
            results.append({
                "id": dbres.data[0]["id"],
                "filename": f.filename,
                "file_type": file_record["file_type"],
                "file_size": len(content),
                "mime_type": mime_type,
                "file_path": storage_path,
                "analysis_id": analysis_id
            })
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error uploading {f.filename}: {str(e)}"
            )
    
    # Автоматически запускаем анализ после загрузки файлов
    try:
        from tasks.analysis_tasks import analyze_cv_background
        analyze_cv_background.delay(analysis_id)
        print(f"✅ Analysis task triggered for analysis_id: {analysis_id}")
    except Exception as e:
        print(f"⚠️ Failed to trigger analysis task: {e}")
    
    return {"files": results, "analysis_id": analysis_id}

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    credentials=Depends(bearer_scheme)
):
    raise HTTPException(status_code=501, detail="File info endpoint temporarily disabled during Supabase migration")

@router.get("/", response_model=FileListResponse)
async def list_files(
    analysis_id: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    credentials=Depends(bearer_scheme)
):
    raise HTTPException(status_code=501, detail="File list endpoint temporarily disabled during Supabase migration")

@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    credentials=Depends(bearer_scheme)
):
    raise HTTPException(status_code=501, detail="File delete endpoint temporarily disabled during Supabase migration")

@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    credentials=Depends(bearer_scheme)
):
    raise HTTPException(status_code=501, detail="File download endpoint temporarily disabled during Supabase migration") 