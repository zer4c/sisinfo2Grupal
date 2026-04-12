from fastapi import APIRouter, status
from src.core.database import SessionDep

from src.modules.subject.schemas import SubjectBase, EnrollmentBase
from src.modules.subject.controllers import SubjectController

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(session: SessionDep, subject_info: SubjectBase):
    return await SubjectController.create_subject(session, subject_info)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_subjects_for_teacher(session: SessionDep, teacher_id: int):
    return await SubjectController.get_all_subjects_for_teacher(session, teacher_id)

@router.post(
    "/enrollment",
    status_code=status.HTTP_201_CREATED,
)
async def enrollment_class(session: SessionDep, enrollment: EnrollmentBase):
    return await SubjectController.enrollment_class(session, enrollment)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def read_subject(session: SessionDep, id: int):
    return await SubjectController.read_subject(session, id)