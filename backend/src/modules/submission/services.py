from sqlalchemy import select
from src.core.database import SessionDep

from src.modules.submission.model import SubmissionFile, Submission
from src.modules.submission.schemas import (
    SubmissionFileResponse,
    SubmissionFileCreate,
    SubmissionResponse
)


class SubmissionService:
    @staticmethod
    async def create_file_submission(session: SessionDep, submission_file_data: SubmissionFile):
        try:
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
    
    @staticmethod
    async def get_submissions_done(session: SessionDep, assignment_id: int):
        try:
            result = await session.execute(
                select(Submission).
                where(Submission.assignment_id == assignment_id 
                      and Submission.state_id == 2)
            )
            done_orm = result.scalars().all()
            return [SubmissionResponse.model_validate(s) for s in done_orm]
        except Exception:
            raise
