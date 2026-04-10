from pydantic import BaseModel, ConfigDict
from datetime import date


class SubjectBase(BaseModel):
    code: str 
    period: date
    teacher_id: int
    name: str
    description: str | None = None
    max_students: int

class SubjectResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    id: int
    code: str
    period: date
    teacher_id: int
    name: str
    description: str | None = None
    max_students: int
    