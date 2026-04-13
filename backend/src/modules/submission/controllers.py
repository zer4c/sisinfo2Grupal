from fastapi import HTTPException, UploadFile
from src.core.database import SessionDep

from src.modules.submission.services import SubmissionService
from src.modules.submission.schemas import (
    SubmissionFileCreate,
    SubmissionFile,
)
from src.core.files_database import FileParser


class SubmissionController:
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
    
    @staticmethod
    async def get_submissions_done(session: SessionDep, assignment_id: int):
        submissions_done = await SubmissionService.get_submissions_done(session, assignment_id)
        if not submissions_done:
            raise HTTPException(status_code=404, detail="Submissions done not found")
        return {"message": "submissions found", "ok":True, "data":submissions_done}
