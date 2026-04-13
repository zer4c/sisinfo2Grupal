from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from src.core.enum import FileTypeEnum


class CommentFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_file: FileTypeEnum


class SubmissionCommentBase(BaseModel):
    comment: str = Field(..., min_length=1, max_length=2000)
    teacher_id: int


class SubmissionCommentCreate(SubmissionCommentBase):
    pass


class SubmissionCommentUpdate(BaseModel):
    comment: str = Field(..., min_length=1, max_length=2000)


class SubmissionCommentResponse(SubmissionCommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    submission_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    files: List[CommentFileResponse] = []


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    submission_id: int
    comment_id: int
    student_id: int
    is_read: bool
