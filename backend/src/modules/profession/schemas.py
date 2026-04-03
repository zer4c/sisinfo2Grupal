from pydantic import BaseModel
from pydantic import ConfigDict


class ProfessionBase(BaseModel):
    name: str
    position: int
    salary: int

class ProfessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    position: int
    salary: int








    