from datetime import date
from sqlalchemy import select
from src.core.database import SessionDep

from src.modules.submission.model import Submission, SubmissionFile
from src.modules.assignment.model import Assignment
from src.modules.submission.schemas import (
    SubmissionResponse,
    SubmissionBase,
    SubmissionFileResponse,
    SubmissionFileCreate
)


class SubmissionService:
    @staticmethod
    async def create_submission(session: SessionDep, submission_info: SubmissionBase):
        try:
            assignment_result = await session.execute(
                select(Assignment).where(Assignment.id == submission_info.assignment_id)
            )
            assignment_orm = assignment_result.scalars().one_or_none()

            if not assignment_orm:
                return "assignment not found"

            if date.today() > assignment_orm.due_date:
                return "deadline passed"

            new_submission = Submission(
                student_id=submission_info.student_id,
                assignment_id=submission_info.assignment_id,
                state_id=submission_info.state_id,
                grade=submission_info.grade
            )
            session.add(new_submission)
            await session.commit()
            await session.refresh(new_submission)
            return SubmissionResponse.model_validate(new_submission)
        except Exception:
            session.rollback()
            raise

    @staticmethod
    async def create_file_submission(session: SessionDep, submission_file_data):
        try:
            submission_result = await session.execute(
                select(Submission).where(Submission.id == submission_file_data.submission_id)
            )
            submission_orm = submission_result.scalars().one_or_none()
            if not submission_orm:
                return "submission not found"

            assignment_result = await session.execute(
                select(Assignment).where(Assignment.id == submission_orm.assignment_id)
            )
            assignment_orm = assignment_result.scalars().one_or_none()

            if assignment_orm and date.today() > assignment_orm.due_date:
                return "deadline passed"

            new_file = SubmissionFile(
                submission_id=submission_file_data.submission_id,
                type_file=submission_file_data.type_file,
                data=submission_file_data.data,
            )
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
            return SubmissionFileResponse.model_validate(new_file)
        except Exception:
            session.rollback()
            raise

    @staticmethod
    async def get_file_submission(session: SessionDep, id_file: int):
        try:
            result = await session.execute(
                select(SubmissionFile).where(SubmissionFile.id == id_file)
            )
            file_orm = result.scalars().one_or_none()
            if not file_orm:
                return None
            return SubmissionFileCreate.model_validate(file_orm)
        except Exception:
            raise

    @staticmethod
    async def get_all_file_by_submission(session: SessionDep, id_submission: int):
        try:
            result = await session.execute(
                select(SubmissionFile).where(
                    SubmissionFile.submission_id == id_submission
                )
            )
            files_orm = result.scalars().all()
            return [SubmissionFileResponse.model_validate(f) for f in files_orm]
        except Exception:
            raise
