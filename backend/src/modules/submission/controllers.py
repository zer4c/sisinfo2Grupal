from fastapi import HTTPException, UploadFile
from src.core.database import SessionDep

from src.modules.submission.services import SubmissionService
from src.modules.submission.schemas import (
    SubmissionBase,
    SubmissionFileCreate,
    SubmissionFile,
)
from src.core.files_database import FileParser


class SubmissionController:
    @staticmethod
    async def create_submission(session: SessionDep, submission_info: SubmissionBase):
        submission = await SubmissionService.create_submission(session, submission_info)
        
        if submission == "assignment not found":
            raise HTTPException(status_code=404, detail="Assignment not found")
            
        if submission == "deadline passed":
            raise HTTPException(status_code=403, detail="The deadline for this assignment has passed")
            
        return {"message": "submission created", "ok": True, "data": submission}

    @staticmethod
    async def create_file_submission(
        session: SessionDep, submission_data: SubmissionFile, data: UploadFile
    ):
        try:
            submission_file_data = await SubmissionFileCreate(
                submission_id=submission_data.submission_id,
                type_file=submission_data.type_file,
                data=await FileParser.to_bytes(data),
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Error processing file")
        id_file = await SubmissionService.create_file_submission(
            session, submission_file_data
        )

        if id_file == "submission not found":
            raise HTTPException(status_code=404, detail="Submission not found")
        if id_file == "deadline passed":
            raise HTTPException(status_code=403, detail="The deadline for this assignment has passed.")

        return {"message": "file created", "ok": True, "data": id_file}

    @staticmethod
    async def get_file_submission(session: SessionDep, id_file: int):
        file_submission = await SubmissionService.get_file_submission(session, id_file)
        if not file_submission:
            raise HTTPException(status_code=404, detail="File submission not found")
        return FileParser.to_response(
            file_submission.data, f"submission_file_{id_file}"
        )

    @staticmethod
    async def get_all_file_by_submission(session: SessionDep, id_submission: int):
        files_submission = await SubmissionService.get_all_file_by_submission(
            session, id_submission
        )
        return {"message": "files found", "ok": True, "data": files_submission}
