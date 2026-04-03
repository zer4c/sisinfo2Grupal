from pydantic import BaseModel

class ProfesionCreate(BaseModel):
    name: str
    position: int
    salary: int

class ProfesionResponse(ProfesionCreate):
    id: int

    model_config = {"from_attributes": True}