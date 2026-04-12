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