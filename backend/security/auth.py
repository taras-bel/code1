"""
Authentication and authorization utilities
"""
import os
import logging
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from supabase import create_client, Client
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

logger = logging.getLogger(__name__)

# Supabase клиент
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_secret_key() -> str:
    """Получает секретный ключ для JWT"""
    if not SECRET_KEY or SECRET_KEY == "your-secret-key-here":
        raise RuntimeError("SECRET_KEY must be set in environment variables!")
    return SECRET_KEY

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str) -> str:
    """Декодирует JWT и возвращает user_id, либо выбрасывает HTTPException"""
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_user_exists(user_id: str) -> bool:
    """Проверяет существование пользователя в Supabase"""
    try:
        resp = supabase.table("profiles").select("id").eq("id", user_id).single().execute()
        return bool(resp.data)
    except Exception as e:
        logger.error(f"Error verifying user {user_id}: {e}")
        return False

def get_user_profile(user_id: str) -> Optional[dict]:
    """Получает профиль пользователя из Supabase"""
    try:
        resp = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return resp.data if resp.data else None
    except Exception as e:
        logger.error(f"Error getting user profile {user_id}: {e}")
        return None

def create_user_profile(user_data: dict) -> Optional[dict]:
    """Создает профиль пользователя в Supabase"""
    try:
        resp = supabase.table("profiles").insert(user_data).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error creating user profile: {e}")
        return None

def update_user_profile(user_id: str, profile_data: dict) -> Optional[dict]:
    """Обновляет профиль пользователя в Supabase"""
    try:
        resp = supabase.table("profiles").update(profile_data).eq("id", user_id).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error updating user profile {user_id}: {e}")
        return None

def check_rate_limit(user_id: str, action: str) -> bool:
    """Проверяет лимиты использования для пользователя"""
    try:
        # Получаем текущие лимиты пользователя
        resp = supabase.table("rate_limits").select("*").eq("user_id", user_id).eq("action", action).single().execute()
        
        if not resp.data:
            # Создаем новую запись лимита
            limit_data = {
                "user_id": user_id,
                "action": action,
                "count": 1,
                "reset_at": datetime.utcnow() + timedelta(days=7)
            }
            supabase.table("rate_limits").insert(limit_data).execute()
            return True
        
        rate_limit = resp.data
        reset_at = rate_limit.get("reset_at")
        
        # Проверяем, нужно ли сбросить счетчик
        if reset_at and datetime.fromisoformat(reset_at) < datetime.utcnow():
            # Сбрасываем счетчик
            supabase.table("rate_limits").update({
                "count": 1,
                "reset_at": datetime.utcnow() + timedelta(days=7)
            }).eq("id", rate_limit["id"]).execute()
            return True
        
        # Проверяем лимит
        current_count = rate_limit.get("count", 0)
        max_count = 4  # Лимит на неделю
        
        if current_count >= max_count:
            return False
        
        # Увеличиваем счетчик
        supabase.table("rate_limits").update({
            "count": current_count + 1
        }).eq("id", rate_limit["id"]).execute()
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking rate limit for user {user_id}: {e}")
        return True  # В случае ошибки разрешаем действие

# Rate limiting utilities
class RateLimiter:
    """Simple rate limiter for API endpoints"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Check if request is allowed based on rate limit"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[key]) < max_requests:
            self.requests[key].append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, key: str, max_requests: int, window_seconds: int) -> int:
        """Get remaining requests allowed"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        if key not in self.requests:
            return max_requests
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        return max(0, max_requests - len(self.requests[key]))

# Global rate limiter instance
rate_limiter = RateLimiter()

def check_rate_limit_decorator(key: str, max_requests: int = 10, window_seconds: int = 60):
    """Decorator to check rate limit for endpoints"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Password utilities (for future use)
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    # This would be implemented with bcrypt
    # For now, return as-is (not secure for production)
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    # This would be implemented with bcrypt
    # For now, simple comparison (not secure for production)
    return plain_password == hashed_password

# Input validation utilities
def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Basic sanitization - remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Basic phone validation - adjust based on your requirements
    pattern = r'^\+?[\d\s\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None 