"""
Database models for NoaMetrics - Supabase integration
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid

# Pydantic models for Supabase tables
class User(BaseModel):
    """User model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    is_beta_user: bool = False
    beta_company: Optional[str] = None
    beta_role: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Analysis(BaseModel):
    """Analysis model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    job_description: str
    status: str = "pending"  # pending, processing, completed, failed
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None  # in seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UploadedFile(BaseModel):
    """Uploaded file model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_id: str
    filename: str
    file_path: str
    file_type: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    extracted_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RateLimit(BaseModel):
    """Rate limit model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    analysis_count: int = 0
    last_analysis: Optional[datetime] = None
    week_start: datetime
    max_weekly_analyses: int = 4
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(BaseModel):
    """Audit log model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CacheEntry(BaseModel):
    """Cache entry model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str
    value: Dict[str, Any]
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SystemConfig(BaseModel):
    """System configuration model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None
    is_public: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Profile(BaseModel):
    """Profile model for Supabase"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    full_name: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    consent: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 