"""
NoaMetrics Backend API
----------------------
FastAPI backend for NoaMetrics. Handles user registration, login, file upload, and analysis limits using Supabase as the main data store.
"""
# --- Импорты ---
import os
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Any, cast, Union
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Form, Security, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # python-jose
from pydantic import BaseModel, EmailStr
import secrets
import requests
import io
import docx
import PyPDF2
# from cv_analysis.cv_analyzer import CVAnalyzer
from fastapi import Request, Depends
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, EmailStr
from database.models import Profile
# from database.connection import get_db
from supabase import create_client
from api.v1 import router as v1_router
from config import (
    BUCKET_NAME, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, 
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
    CORS_ORIGINS, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
)
from starlette.middleware.base import BaseHTTPMiddleware

class BetaRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    company_name: Optional[str] = None
    role: Optional[str] = None
    consent: bool = True

# --- Константы и конфиг ---
UPLOADED_FILES_TABLE = "uploaded_files"
PROFILES_TABLE = "profiles"
RATE_LIMITS_TABLE = "rate_limits"
MAX_FILE_SIZE_MB = 10
ANALYSIS_LIMIT_PER_WEEK = 4

# --- Логирование ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- Supabase клиент ---
if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL must be set in environment variables!")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY must be set in environment variables!")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_SERVICE_ROLE_KEY: [HIDDEN]")  # Hide sensitive data in production

# --- Supabase REST API helpers ---
# Пример fetch-запроса к таблице Supabase через REST API

def fetch_supabase_table(table: str, params=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Пример fetch-запроса к Supabase Storage (список файлов в бакете)
def fetch_supabase_storage(bucket: str):
    url = f"{SUPABASE_URL}/storage/v1/object/list/{bucket}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# --- FastAPI app ---
app = FastAPI(
    title="NoaMetrics API",
    description="AI-powered CV analysis and candidate comparison platform",
    version="1.0.0"
)

# --- CORS (разрешить фронту на localhost:3000) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware для логирования запросов ---
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        if request.method == "POST":
            try:
                body = await request.body()
                content_type = request.headers.get("content-type", "")
                if body:
                    if (
                        "multipart/form-data" in content_type or
                        "application/octet-stream" in content_type or
                        content_type.startswith("image/") or
                        content_type.startswith("audio/") or
                        content_type.startswith("video/")
                    ):
                        logger.info(f"Request body: <{content_type} - binary data not logged>")
                    else:
                        try:
                            logger.info(f"Request body: {body.decode('utf-8')}")
                        except Exception:
                            logger.info("Request body: <could not decode body as utf-8>")
                # Восстанавливаем body для downstream
                async def receive():
                    return {"type": "http.request", "body": body}
                request._receive = receive
            except Exception as e:
                logger.warning(f"Could not read request body: {e}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)

bearer_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.include_router(v1_router, prefix="/api")

# --- Pydantic модели ---
class UserCreate(BaseModel):
    email: str
    name: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    phone: Optional[str] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AnalysisCreate(BaseModel):
    job_description: str

# --- Вспомогательные функции ---
def get_secret_key() -> str:
    if not SECRET_KEY or SECRET_KEY == "your-secret-key-here":
        raise RuntimeError("SECRET_KEY must be set in environment variables!")
    return SECRET_KEY

def decode_jwt_token(token: str) -> str:
    """Декодирует JWT и возвращает user_id, либо выбрасывает HTTPException."""
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создаёт JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt

# --- Базовые эндпоинты ---
@app.get("/")
def read_root() -> dict:
    """Корневой эндпоинт."""
    return {"message": "NoaMetrics API is running!", "version": "1.0.0"}

@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "message": "NoaMetrics API is running"}

@app.get("/docs")
def get_docs() -> dict:
    """API documentation endpoint."""
    return {"docs_url": "/docs", "openapi_url": "/openapi.json"}

# --- Аутентификация ---
# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     # Этот endpoint удален - логин теперь в auth.py через Supabase Python SDK
#     pass

# @app.post("/register")
# async def register(user_data: UserCreate):
#     # Этот endpoint удален - регистрация теперь в auth.py через Supabase Python SDK
#     pass

# @app.post("/beta-register")
# async def beta_register(beta_data: BetaRegistrationRequest):
#     # Этот endpoint удален - регистрация теперь в auth.py через Supabase Python SDK
#     # Старая логика с /auth/v1/admin/users больше не используется
#     pass

# --- Защищенные эндпоинты ---
async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Получение текущего пользователя из токена."""
    user_id = decode_jwt_token(credentials.credentials)
    # Здесь должна быть загрузка пользователя из Supabase
    return {"id": user_id, "email": "test@example.com", "name": "Test User"}

@app.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Получение данных текущего пользователя."""
    return current_user

@app.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Получение профиля пользователя."""
    # Здесь должна быть загрузка профиля из Supabase
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user["name"],
        "phone": "+1234567890",
        "company": "Test Company",
        "role": "HR Manager"
    }

@app.put("/profile")
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    """Обновление профиля пользователя."""
    # Здесь должно быть обновление в Supabase
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": profile_data.get("name", current_user["name"]),
        "phone": profile_data.get("phone", "+1234567890"),
        "company": profile_data.get("company", "Test Company"),
        "role": profile_data.get("role", "HR Manager")
    }

@app.get("/preferences")
async def get_preferences(current_user: dict = Depends(get_current_user)):
    """Получение настроек пользователя."""
    # Здесь должна быть загрузка настроек из Supabase
    return {
        "language": "en",
        "theme": "light",
        "notifications": True,
        "email_notifications": True
    }

@app.put("/preferences")
async def update_preferences(preferences_data: dict, current_user: dict = Depends(get_current_user)):
    """Обновление настроек пользователя."""
    # Здесь должно быть обновление в Supabase
    return preferences_data

# Эндпоинт /my-analyses перенесен в api/v1/analysis.py

# Эндпоинт /compare-candidates перенесен в api/v1/analysis.py

@app.get("/usage-stats")
async def get_usage_stats(current_user: dict = Depends(get_current_user)):
    """Получение статистики использования."""
    # Здесь должна быть загрузка статистики из Supabase
    return {
        "total_analyses": 15,
        "analyses_this_week": 3,
        "analyses_this_month": 8,
        "remaining_analyses": 1,
        "last_analysis_date": "2024-01-15T10:30:00Z"
    }

@app.get("/test-supabase-table")
def test_supabase_table():
    try:
        data = fetch_supabase_table("profiles")
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-supabase-storage")
def test_supabase_storage():
    try:
        data = fetch_supabase_storage(BUCKET_NAME)
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 