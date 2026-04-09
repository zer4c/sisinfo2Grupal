from src.core.database import SessionDep

from src.modules.subject.schemas import SubjectBase
from src.modules.subject.services import SubjectService

class SubjectController():
    @staticmethod
    async def create_subject(session: SessionDep, subject_info: SubjectBase):
        #subject = await SubjectService.get_subject_by_code(session, subject_info.code)
        #if subject:
           #raise HTTPException(status_code = 404, detail="Subject already exists") uy nose
        subject = await SubjectService.create_subject(session, subject_info)
        return {"message": "subject created", "ok": True, "data": subject}