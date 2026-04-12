from pydantic import BaseModel

class TeacherBase(BaseModel):
    id: int
    name: str

class TeacherResponse(TeacherBase):
    pass