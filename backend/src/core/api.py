from fastapi import APIRouter

from src.modules.subject.routes import router as subject_router

router = APIRouter()

router.include_router(subject_router, prefix="/subject", tags=["subject"])