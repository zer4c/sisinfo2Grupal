from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict
from src.core.enum import FileTypeEnum


class AssignmentBase(BaseModel):
    subject_id: int
    title: str
    description: Optional[str] = None
    due_date: date
    points: int


class AssignmentResponse(AssignmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: date


class AssignmentFile(BaseModel):
    assignment_id: int
    type_file: FileTypeEnum


class AssignmentFileCreate(AssignmentFile):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    data: bytes


class AssignmentFileResponse(AssignmentFile):
    model_config = ConfigDict(from_attributes=True)
    id: int
