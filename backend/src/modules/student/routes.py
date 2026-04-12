from fastapi import APIRouter, status
from src.core.database import SessionDep

from src.modules.student.controllers import StudentController

router = APIRouter()


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def read_student(session: SessionDep, id: int):
    return await StudentController.read_student(session, id)