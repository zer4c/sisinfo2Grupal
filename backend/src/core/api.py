from fastapi import APIRouter
from src.modules.assignment.routes import router as assignment_router
from src.modules.student.routes import router as student_router
from src.modules.subject.routes import router as subject_router
from src.modules.submission.routes import router as submission_router
from src.modules.teacher.routes import router as teacher_router

router = APIRouter()

router.include_router(subject_router, prefix="/subject", tags=["subject"])
router.include_router(student_router, prefix="/student", tags=["student"])
router.include_router(teacher_router, prefix="/teacher", tags=["teacher"])
router.include_router(assignment_router, prefix="/assignment", tags=["assignment"])
router.include_router(submission_router, prefix="/submission", tags=["submission"])
