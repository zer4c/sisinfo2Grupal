from fastapi import APIRouter
from src.modules.profesion.routes import router as profesion_router

router = APIRouter()
router.include_router(profesion_router)