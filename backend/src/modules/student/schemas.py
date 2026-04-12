from pydantic import BaseModel

class StudentBase(BaseModel):
    id: int
    name: str

class StudentResponse(StudentBase):
    pass