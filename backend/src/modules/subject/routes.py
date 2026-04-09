from fastapi import APIRouter, status
from src.core.database import SessionDep

from src.modules.subject.schemas import SubjectBase
from src.modules.subject.controllers import SubjectController

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_subject(session: SessionDep, subject_info: SubjectBase):
    return await SubjectController.create_subject(session, subject_info)