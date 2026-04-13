from datetime import datetime
from sqlalchemy import select
from src.core.database import SessionDep
from src.modules.comments.model import SubmissionComment, CommentFile, Notification
from src.modules.submission.model import Submission
from src.modules.comments.schemas import (
    SubmissionCommentCreate,
    SubmissionCommentResponse,
    SubmissionCommentUpdate,
    CommentFileResponse,
    NotificationResponse,
)
from src.modules.submission.schemas import SubmissionResponse


class CommentService:

    @staticmethod
    async def get_submission_by_id(session: SessionDep, submission_id: int):
        try:
            result = await session.execute(
                select(Submission).where(Submission.id == submission_id)
            )
            submission_orm = result.scalars().one_or_none()
            if not submission_orm:
                return None
            return SubmissionResponse.model_validate(submission_orm)
        except Exception:
            raise

    @staticmethod
    async def create_comment(
        session: SessionDep, submission_id: int, comment_data: SubmissionCommentCreate
    ):
        try:
            new_comment = SubmissionComment(
                submission_id=submission_id,
                teacher_id=comment_data.teacher_id,
                comment=comment_data.comment,
                created_at=datetime.now(),
                updated_at=None,
            )
            session.add(new_comment)
            await session.commit()
            await session.refresh(new_comment)
            return SubmissionCommentResponse.model_validate(new_comment)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_comment_by_id(session: SessionDep, comment_id: int):
        try:
            result = await session.execute(
                select(SubmissionComment).where(SubmissionComment.id == comment_id)
            )
            comment_orm = result.scalars().one_or_none()
            if not comment_orm:
                return None
            return SubmissionCommentResponse.model_validate(comment_orm)
        except Exception:
            raise

    @staticmethod
    async def update_comment(
        session: SessionDep, comment_id: int, comment_data: SubmissionCommentUpdate
    ):
        try:
            result = await session.execute(
                select(SubmissionComment).where(SubmissionComment.id == comment_id)
            )
            comment_orm = result.scalars().one_or_none()
            if not comment_orm:
                return None
            
            comment_orm.comment = comment_data.comment
            comment_orm.updated_at = datetime.now()
            
            await session.commit()
            await session.refresh(comment_orm)
            return SubmissionCommentResponse.model_validate(comment_orm)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def delete_comment(session: SessionDep, comment_id: int):
        try:
            result = await session.execute(
                select(SubmissionComment).where(SubmissionComment.id == comment_id)
            )
            comment_orm = result.scalars().one_or_none()
            if not comment_orm:
                return None
            
            await session.delete(comment_orm)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_all_comments_by_submission(session: SessionDep, submission_id: int):
        try:
            result = await session.execute(
                select(SubmissionComment)
                .where(SubmissionComment.submission_id == submission_id)
                .order_by(SubmissionComment.created_at.desc())
            )
            comments_orm = result.scalars().all()
            return [SubmissionCommentResponse.model_validate(c) for c in comments_orm]
        except Exception:
            raise

    @staticmethod
    async def create_comment_file(
        session: SessionDep, comment_id: int, file_data: bytes, file_type: str
    ):
        try:
            new_file = CommentFile(
                comment_id=comment_id,
                data=file_data,
                type_file=file_type,
            )
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
            return CommentFileResponse.model_validate(new_file)
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def get_comment_file(session: SessionDep, file_id: int):
        try:
            result = await session.execute(
                select(CommentFile).where(CommentFile.id == file_id)
            )
            file_orm = result.scalars().one_or_none()
            if not file_orm:
                return None
            return file_orm
        except Exception:
            raise

    @staticmethod
    async def get_all_files_by_comment(session: SessionDep, comment_id: int):
        try:
            result = await session.execute(
                select(CommentFile).where(CommentFile.comment_id == comment_id)
            )
            files_orm = result.scalars().all()
            return [CommentFileResponse.model_validate(f) for f in files_orm]
        except Exception:
            raise

    @staticmethod
    async def delete_comment_file(session: SessionDep, file_id: int):
        try:
            result = await session.execute(
                select(CommentFile).where(CommentFile.id == file_id)
            )
            file_orm = result.scalars().one_or_none()
            if not file_orm:
                return None
            
            await session.delete(file_orm)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def create_notification(
        session: SessionDep,
        submission_id: int,
        comment_id: int,
        student_id: int,
    ):
        try:
            new_notification = Notification(
                submission_id=submission_id,
                comment_id=comment_id,
                student_id=student_id,
                is_read=False,
            )
            session.add(new_notification)
            await session.commit()
            await session.refresh(new_notification)
            return NotificationResponse.model_validate(new_notification)
        except Exception:
            await session.rollback()
            raise
