from pydantic import BaseModel, ConfigDict
from typing import Optional

class StudentBase(BaseModel):
    name: str
    age: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

class StudentResponse(StudentBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)