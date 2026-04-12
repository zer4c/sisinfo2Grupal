from fastapi import APIRouter, status
from src.core.database import SessionDep

from src.modules.assignment.schemas import AssignmentBase
from src.modules.assignment.controllers import AssignmentController

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_assignment(session: SessionDep, assignment_info: AssignmentBase):
    return await AssignmentController.create_assignment(session, assignment_info)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_assignments_for_subject(session: SessionDep, subject_id: int):
    return await AssignmentController.get_all_assignments_for_subject(session, subject_id)

@router.get(
    "/{assignment_id}",
    status_code=status.HTTP_200_OK,
)
async def read_assignment(session: SessionDep, assignment_id: int):
    return await AssignmentController.read_assignment(session, assignment_id)