from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.core.enum import FileTypeEnum

class SubmissionBase(BaseModel):
    assignment_id: int
    student_id: int
    state_id: int 
    grade: Optional[int] = None


class SubmissionResponse(SubmissionBase):
    id: int 
    model_config = ConfigDict(from_attributes=True)

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

class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    assignment_id: int
    state_id: int
    grade: int