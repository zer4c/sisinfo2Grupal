from fastapi import APIRouter, status, File, UploadFile, Form
from typing import Annotated

from src.core.database import SessionDep
from src.modules.assignment.schemas import AssignmentBase, AssignmentFile
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
    return await AssignmentController.get_all_assignments_for_subject(
        session, subject_id
    )


@router.get(
    "/{assignment_id}",
    status_code=status.HTTP_200_OK,
)
async def read_assignment(session: SessionDep, assignment_id: int):
    return await AssignmentController.read_assignment(session, assignment_id)


@router.post(
    "/{id_assignment}/file",
    status_code=status.HTTP_200_OK,
)
async def create_file_assignment(
    assignment_data: Annotated[AssignmentFile, Form()],
    session: SessionDep,
    data: UploadFile = File(...),
):
    return await AssignmentController.create_file_assignment(
        session, assignment_data, data
    )


@router.get(
    "/{id_assignment}/file/{id_file}",
    status_code=status.HTTP_200_OK,
)
async def get_file_assignment(session: SessionDep, id_file: int):
    return await AssignmentController.get_file_assignment(session, id_file)


@router.get("/{id_assignment}/file/", status_code=status.HTTP_200_OK)
async def get_all_file_by_assignment(session: SessionDep, id_assignment: int):
    return await AssignmentController.get_all_file_by_assignment(session, id_assignment)
