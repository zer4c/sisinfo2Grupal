from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class AssignmentBase(BaseModel):
    subject_id: int
    title: str
    description: Optional[str] = None
    due_date: date
    points: int

class AssignmentResponse(AssignmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: date  