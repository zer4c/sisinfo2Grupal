from datetime import date, timedelta
from fastapi import HTTPException, UploadFile
from src.core.database import SessionDep
from src.core.files_database import FileParser
from src.core.enum import FileTypeEnum
from src.modules.comments.schemas import (
    SubmissionCommentCreate,
    SubmissionCommentUpdate,
)
from src.modules.comments.services import CommentService


class CommentController:
    @staticmethod
    async def create_comment(
        session: SessionDep,
        submission_id: int,
        comment_data: SubmissionCommentCreate,
    ):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.create_comment(
            session, submission_id, comment_data
        )

        await CommentService.create_notification(
            session, submission_id, comment.id, submission.student_id
        )

        return {
            "message": "Comment created successfully",
            "ok": True,
            "data": comment,
        }

    @staticmethod
    async def get_comment(session: SessionDep, submission_id: int, comment_id: int):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        return {"message": "Comment found", "ok": True, "data": comment}

    @staticmethod
    async def get_all_comments(session: SessionDep, submission_id: int):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comments = await CommentService.get_all_comments_by_submission(
            session, submission_id
        )

        return {
            "message": "Comments found",
            "ok": True,
            "data": comments,
        }

    @staticmethod
    async def update_comment(
        session: SessionDep,
        submission_id: int,
        comment_id: int,
        comment_data: SubmissionCommentUpdate,
    ):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        now = date.today()
        elapsed_time = now - comment.created_at
        if elapsed_time > timedelta(days=2):
            raise HTTPException(
                status_code=403,
                detail="Cannot edit comment after 48 hours",
            )

        updated_comment = await CommentService.update_comment(
            session, comment_id, comment_data
        )

        return {
            "message": "Comment updated successfully",
            "ok": True,
            "data": updated_comment,
        }

    @staticmethod
    async def delete_comment(session: SessionDep, submission_id: int, comment_id: int):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        now = date.today()
        elapsed_time = now - comment.created_at
        if elapsed_time > timedelta(days=2):
            raise HTTPException(
                status_code=403,
                detail="Cannot delete comment after 48 hours",
            )

        await CommentService.delete_comment(session, comment_id)

        return {
            "message": "Comment deleted successfully",
            "ok": True,
        }

    @staticmethod
    async def add_file_to_comment(
        session: SessionDep,
        submission_id: int,
        comment_id: int,
        file_data: UploadFile,
        file_type: FileTypeEnum,
    ):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        now = date.today()
        elapsed_time = now - comment.created_at
        if elapsed_time > timedelta(days=2):
            raise HTTPException(
                status_code=403,
                detail="Cannot add files to comment after 48 hours",
            )

        existing_files = await CommentService.get_all_files_by_comment(
            session, comment_id
        )
        if len(existing_files) >= 3:
            raise HTTPException(
                status_code=400,
                detail="Maximum 3 files per comment reached",
            )

        try:
            file_bytes = await FileParser.to_bytes(file_data)
        except Exception:
            raise HTTPException(status_code=500, detail="Error processing file")

        MAX_FILE_SIZE = 20 * 1024 * 1024
        if file_data.size is not None and file_data.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File is too large. Maximum size allowed is 20MB."
            )

        created_file = await CommentService.create_comment_file(
            session, comment_id, file_bytes, file_type
        )

        return {
            "message": "File added successfully",
            "ok": True,
            "data": created_file,
        }

    @staticmethod
    async def get_file_from_comment(
        session: SessionDep, submission_id: int, comment_id: int, file_id: int
    ):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        file_data = await CommentService.get_comment_file(session, file_id)
        if not file_data or file_data.comment_id != comment_id:
            raise HTTPException(status_code=404, detail="File not found")

        return FileParser.to_response(file_data.data, f"comment_file_{file_id}.{file_data.type_file.value}")

    @staticmethod
    async def get_all_files_by_comment(
        session: SessionDep, submission_id: int, comment_id: int
    ):
        submission = await CommentService.get_submission_by_id(
            session, submission_id
        )
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        comment = await CommentService.get_comment_by_id(session, comment_id)
        if not comment or comment.submission_id != submission_id:
            raise HTTPException(status_code=404, detail="Comment not found")

        files = await CommentService.get_all_files_by_comment(
            session, comment_id
        )

        return {
            "message": "Files found",
            "ok": True,
            "data": files,
        }
