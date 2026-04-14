from datetime import date

from fastapi import HTTPException, UploadFile
from src.core.database import SessionDep
from src.core.files_database import FileParser
from src.modules.assignment.services import AssignmentService
from src.modules.submission.schemas import (
    SubmissionBase,
    SubmissionFile,
    SubmissionFileCreate,
)
from src.modules.submission.services import SubmissionService


class SubmissionController:
    @staticmethod
    async def create_submission(session: SessionDep, submission_info: SubmissionBase):
        assignment = await AssignmentService.get_assignment_by_id(
            session, submission_info.assignment_id
        )
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        if date.today() > assignment.due_date:
            raise HTTPException(
                status_code=403, detail="The deadline for this assignment has passed"
            )

        submission = await SubmissionService.create_submission(session, submission_info)
        return {"message": "submission created", "ok": True, "data": submission}

    @staticmethod
    async def create_file_submission(
        session: SessionDep, submission_data: SubmissionFile, data: UploadFile
    ):
        try:
            submission_file_data = SubmissionFileCreate(
                submission_id=submission_data.submission_id,
                type_file=submission_data.type_file,
                data=await FileParser.to_bytes(data),
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Error processing file")
        id_file = await SubmissionService.create_file_submission(
            session, submission_file_data
        )

        submission = await SubmissionService.get_submission_by_id(
            session, submission_data.submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        assignment = await AssignmentService.get_assignment_by_id(
            session, submission.assignment_id
        )
        if not assignment:
            raise HTTPException(
                status_code=404, detail="Assignment not found for this submission"
            )
        if date.today() > assignment.due_date:
            raise HTTPException(
                status_code=403, detail="The deadline for this assignment has passed."
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
        submissions_done = await SubmissionService.get_submissions_done(
            session, assignment_id
        )
        if not submissions_done:
            raise HTTPException(status_code=404, detail="Submissions done not found")
        return {"message": "submissions found", "ok": True, "data": submissions_done}

    @staticmethod
    async def get_submission_by_student(
        session: SessionDep, student_id: int, assignment_id: int
    ):
        submission = await SubmissionService.get_submssion_by_student(
            session, student_id, assignment_id
        )
        if not submission:
            return {"message": "no submission", "ok": True, "data": None}
        return {"message": "submission found", "ok": True, "data": submission}
