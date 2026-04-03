from fastapi import APIRouter

from src.modules.profession.routes import router as profession_router

router = APIRouter()

router.include_router(profession_router, prefix="/profession", tags=["profession"])