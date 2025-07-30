"""
Authentication endpoints for API v1
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
import os
from supabase import create_client, Client

# from database.connection import get_db  # Commented out - not needed with Supabase SDK
from database.models import User, Profile
from security.auth import (
    create_access_token,
    decode_jwt_token,
    get_secret_key,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

# Security
bearer_scheme = HTTPBearer()

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

class BetaRegistrationRequest(BaseModel):
    full_name: str
    email: str  # Временно используем str вместо EmailStr для отладки
    phone: str
    company_name: Optional[str] = None
    role: Optional[str] = None
    consent: bool = True

class ProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    consent: bool
    created_at: str
    updated_at: str
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

# @router.post("/register", response_model=TokenResponse)
# async def register(user_data: UserCreate, db=Depends(get_db)):
#     """
#     Register a new user
#     """
#     # Check if user already exists
#     existing_user = db.query(User).filter(User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists"
#         )
#     # Create new user
#     user = User(
#         email=user_data.email,
#         full_name=user_data.full_name,
#         phone=user_data.phone
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     # Create access token
#     access_token = create_access_token(
#         data={"sub": str(user.id)},
#         expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     return TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
#     )

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/beta-register", response_model=TokenResponse)
async def beta_register(beta_data: BetaRegistrationRequest):
    import logging
    logger = logging.getLogger(__name__)
    logger.info("=== BETA REGISTER CALLED ===")
    logger.info(f"Raw data: {beta_data}")
    logger.info(f"Full name: {beta_data.full_name}")
    logger.info(f"Email: {beta_data.email}")
    logger.info(f"Phone: {beta_data.phone}")
    logger.info(f"Company: {beta_data.company_name}")
    logger.info(f"Role: {beta_data.role}")
    logger.info(f"Consent: {beta_data.consent}")
    logger.info("Validation passed successfully!")
    try:
        # Проверка на существование email
        existing = supabase.table("profiles").select("id").eq("email", beta_data.email).execute()
        if existing.data and len(existing.data) > 0:
            # Если пользователь уже есть — логиним
            profile = existing.data[0]
            access_token = create_access_token(
                data={"sub": str(profile["id"])} ,
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        # Вставка нового профиля
        insert_data = {
            "email": beta_data.email,
            "full_name": beta_data.full_name,
            "phone": beta_data.phone,
            "company_name": beta_data.company_name,
            "role": beta_data.role,
            "consent": beta_data.consent
        }
        result = supabase.table("profiles").insert(insert_data).execute()
        error = getattr(result, 'error', None)
        if error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {error.message if hasattr(error, 'message') else error}")
        profile = result.data[0] if result.data else None

        if not profile:
            raise HTTPException(status_code=500, detail="Failed to create profile")

        # Автоматически логиним пользователя после регистрации
        access_token = create_access_token(
            data={"sub": str(profile["id"])},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in beta registration: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to register for beta program: {e}")

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Passwordless login by email or phone (Profile table via Supabase SDK)
    """
    if not login_data.email and not login_data.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required for login"
        )
    try:
        query = supabase.table("profiles").select("*")
        if login_data.email:
            result = query.eq("email", login_data.email).execute()
        else:
            result = query.eq("phone", login_data.phone).execute()
        profiles = result.data if hasattr(result, 'data') else []
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Profile not found"
            )
        profile = profiles[0]
        access_token = create_access_token(
            data={"sub": str(profile["id"])} ,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to login: {e}")

@router.get("/me", response_model=ProfileResponse)
async def get_current_profile(credentials=Depends(bearer_scheme)):
    """
    Get current profile information (Profile table via Supabase SDK)
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        result = supabase.table("profiles").select("*").eq("id", profile_id).execute()
        profiles = result.data if hasattr(result, 'data') else []
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        return profiles[0]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {e}")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(credentials=Depends(bearer_scheme)):
    """
    Refresh access token (Profile table via Supabase SDK)
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        result = supabase.table("profiles").select("*").eq("id", profile_id).execute()
        profiles = result.data if hasattr(result, 'data') else []
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        access_token = create_access_token(
            data={"sub": str(profile_id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh token: {e}")

@router.post("/logout")
async def logout(
    credentials=Depends(bearer_scheme)
):
    """
    Logout user (invalidate token)
    """
    # In a real implementation, you would add the token to a blacklist
    # For now, we'll just return success
    return {"message": "Successfully logged out"} 