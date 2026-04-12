from fastapi import APIRouter, status, File, UploadFile
from src.core.database import SessionDep

from src.modules.assignment.schemas import AssignmentBase
from src.modules.assignment.controllers import AssignmentController
from src.core.files_database import FileParser

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

@router.post(
    "/test-file-conversion",
    status_code=status.HTTP_200_OK,
)
async def test_file_conversion(file: UploadFile = File(...)):
    file_in_bytes = await FileParser.to_bytes(file)
    
    return FileParser.to_response(
        file_bytes=file_in_bytes, 
        filename=f"copia_{file.filename}",
        media_type=file.content_type
    )