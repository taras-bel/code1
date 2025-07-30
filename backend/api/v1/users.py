"""
User management endpoints for API v1
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from datetime import datetime

# from database.connection import get_db  # Commented out - not needed with Supabase SDK
from database.models import User, Analysis, RateLimit
from security.auth import decode_jwt_token, hash_password, verify_password

router = APIRouter()

# Security
bearer_scheme = HTTPBearer()

# Pydantic models
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserStatsResponse(BaseModel):
    total_analyses: int
    completed_analyses: int
    failed_analyses: int
    success_rate: float
    weekly_analyses_used: int
    weekly_analyses_limit: int
    last_analysis_date: Optional[datetime] = None

# Все endpoints в этом файле используют устаревшую модель User и не должны использоваться.
# Вся логика профиля и аутентификации теперь реализована через Profile в auth.py
# Файл можно удалить или оставить пустым для совместимости. 