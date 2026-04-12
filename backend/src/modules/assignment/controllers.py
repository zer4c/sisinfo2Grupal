from fastapi import HTTPException
from src.core.database import SessionDep

from .services import AssignmentService
from .schemas import AssignmentBase

class AssignmentController:
    @staticmethod
    async def create_assignment(session: SessionDep, assignment_info: AssignmentBase):
        assignment = await AssignmentService.get_by_title_and_subject(
            session, 
            assignment_info.title, 
            assignment_info.subject_id
        )
        if assignment:
            raise HTTPException(status_code = 400, detail="Assignment already exists")
        assignment = await AssignmentService.create_assignment(session, assignment_info)
        return {"message": "assignment created", "ok": True, "data": assignment}
    
    @staticmethod
    async def get_assignments_for_subject(session: SessionDep, id_subject: int):
        assigments = await AssignmentService.get_all_assignment_for_subject(
            session, id_subject
        )
        if not assigments:
            raise HTTPException(status_code=404, detail="Assignments not found")
        return {"message": "assignments found", "ok": True, "detail": assigments}