from datetime import date

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    code: str
    period: date
    teacher_id: int
    name: str
    description: str | None = None
    max_students: int


class SubjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    period: date
    teacher_id: int
    name: str
    description: str | None = None
    max_students: int


class EnrollmentBase(BaseModel):
    id_subject: int
    id_student: int


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_student: int
    id_subject: int
