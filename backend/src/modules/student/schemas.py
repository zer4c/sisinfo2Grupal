from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    id: int
    name: str


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)
