from fastapi import HTTPException
from src.core.database import SessionDep

from src.modules.subject.schemas import SubjectBase
from src.modules.subject.services import SubjectService

class SubjectController():
    @staticmethod
    async def create_subject(session: SessionDep, subject_info: SubjectBase):
        subject = await SubjectService.get_subject_by_name(session, subject_info.name)
        if subject:
           raise HTTPException(status_code = 404, detail="Subject already exists") 
        subject = await SubjectService.create_subject(session, subject_info)
        return {"message": "subject created", "ok": True, "data": subject}