from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from src.core.enum import FileTypeEnum


class CommentFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_file: FileTypeEnum


class SubmissionCommentCreate(BaseModel):
    comment: Optional[str] = None


class SubmissionCommentUpdate(BaseModel):
    comment: Optional[str] = None


class SubmissionCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    submission_id: int
    comment: Optional[str] = None
    created_at: date
    files: List[CommentFileResponse] = []


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    submission_id: int
    comment_id: int
    student_id: int
