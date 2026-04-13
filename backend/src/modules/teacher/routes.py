from fastapi import APIRouter, status
from src.core.database import SessionDep
from src.modules.teacher.controllers import TeacherController

router = APIRouter()


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def read_teacher(session: SessionDep, id: int):
    return await TeacherController.get_teacher(session, id)
