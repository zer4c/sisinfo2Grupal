from fastapi import APIRouter
from src.modules.student.routes import router as students_router

router = APIRouter()

router.include_router(students_router, prefix="/api", tags=["Estudiantes"])