from fastapi import APIRouter
from src.modules.student.routes import router as students_router

from src.modules.subject.routes import router as subject_router

router = APIRouter()

router.include_router(subject_router, prefix="/subject", tags=["subject"])

router.include_router(students_router, prefix="/api", tags=["Estudiantes"])
