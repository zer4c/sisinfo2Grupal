from pydantic import BaseModel, ConfigDict
from src.core.enum import FileTypeEnum


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
