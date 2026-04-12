from fastapi import HTTPException, UploadFile
from src.core.database import SessionDep

from src.modules.assignment.services import AssignmentService
from src.modules.assignment.schemas import (
    AssignmentBase,
    AssignmentFileCreate,
    AssignmentFile,
)
from src.core.files_database import FileParser


class AssignmentController:
    @staticmethod
    async def create_assignment(session: SessionDep, assignment_info: AssignmentBase):
        assignment = await AssignmentService.get_by_title_and_subject(
            session, assignment_info.title, assignment_info.subject_id
        )
        if assignment:
            raise HTTPException(status_code=400, detail="Assignment already exists")
        assignment = await AssignmentService.create_assignment(session, assignment_info)
        return {"message": "assignment created", "ok": True, "data": assignment}

    @staticmethod
    async def read_assignment(session: SessionDep, assignment_id: int):
        assignment = await AssignmentService.get_assignment_by_id(
            session, assignment_id
        )
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return {"message": "assignment found", "ok": True, "data": assignment}

    @staticmethod
    async def get_all_assignments_for_subject(session: SessionDep, subject_id: int):
        assignments = await AssignmentService.get_all_assignments_for_subject(
            session, subject_id
        )
        if not assignments:
            raise HTTPException(status_code=404, detail="Assignments not found")
        return {"message": "assignments found", "ok": True, "data": assignments}

    async def create_file_assignment(
        session: SessionDep, assignment_data: AssignmentFile, data: UploadFile
    ):
        try:
            assignment_file_data = await AssignmentFileCreate(
            assignment_id=assignment_data.assignment_id,
            type_file=assignment_data.type_file,
            data=await FileParser.to_bytes(data),
        )
        except Exception:
            raise HTTPException(status_code=500, detail="Error processing file")
        id_file = await AssignmentService.create_file_assignment(
            session, assignment_file_data
        )
        return {"message": "file created", "ok": True, "data": id_file}
