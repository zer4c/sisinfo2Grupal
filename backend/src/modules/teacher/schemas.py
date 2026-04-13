from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
    id: int
    name: str


class TeacherResponse(TeacherBase):
    model_config = ConfigDict(from_attributes=True)
