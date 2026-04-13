from typing import Optional

from pydantic import BaseModel, ConfigDict
from src.core.enum import FileTypeEnum


class SubmissionBase(BaseModel):
    student_id: int
    assignment_id: int


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    assignment_id: int
    state_id: int
    assignment_id: int
    student_id: int
    state_id: int
    grade: Optional[int] = None


class SubmissionFile(BaseModel):
    submission_id: int
    type_file: FileTypeEnum


class SubmissionFileCreate(SubmissionFile):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data: bytes


class SubmissionFileResponse(SubmissionFile):
    model_config = ConfigDict(from_attributes=True)
    id: int
