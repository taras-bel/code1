"""
API v1 initialization
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .files import router as files_router
from .analysis import router as analysis_router
# from .users import router as users_router  # Temporarily disabled during Supabase migration

# Create v1 router
router = APIRouter(prefix="/v1")

# Include all v1 endpoints
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
router.include_router(files_router, prefix="/files", tags=["Files"])
# router.include_router(users_router, prefix="/users", tags=["Users"])  # Temporarily disabled 