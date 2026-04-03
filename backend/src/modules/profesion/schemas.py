from pydantic import BaseModel


class ProfesionCreate(BaseModel):
    name: str
    position: int
    salary: float


class ProfesionOut(BaseModel):
    id: int
    name: str
    position: int
    salary: float