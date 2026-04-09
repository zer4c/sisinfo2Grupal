from fastapi import APIRouter, status
from src.core.database import SessionDep

from src.modules.student.schemas import StudentCreate, StudentUpdate
from src.modules.student.controllers import StudentController

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_student(session: SessionDep, student_info: StudentCreate):
    return await StudentController.create(session, student_info)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_students(session: SessionDep):
    return await StudentController.get_all(session)

@router.get(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
)
async def get_student(student_id: int, session: SessionDep):
    return await StudentController.get_by_id(session, student_id)

@router.put(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
)
async def update_student(student_id: int, student_info: StudentUpdate, session: SessionDep):
    return await StudentController.update(session, student_id, student_info)

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_student(student_id: int, session: SessionDep):
    return await StudentController.delete(session, student_id)