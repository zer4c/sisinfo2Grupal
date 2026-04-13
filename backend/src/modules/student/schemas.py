from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    id: int
    name: str


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    submission_id: int
    comment_id: int
    student_id: int
