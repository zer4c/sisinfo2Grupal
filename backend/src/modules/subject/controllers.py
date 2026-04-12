from fastapi import HTTPException
from src.core.database import SessionDep

from src.modules.subject.schemas import SubjectBase, EnrollmentBase
from src.modules.subject.services import SubjectService

class SubjectController():
    @staticmethod
    async def create_subject(session: SessionDep, subject_info: SubjectBase):
        subject = await SubjectService.get_subject_by_name(session, subject_info.name)
        if subject:
           raise HTTPException(status_code = 400, detail="Subject already exists") 
        subject = await SubjectService.create_subject(session, subject_info)
        return {"message": "subject created", "ok": True, "data": subject}
    
    @staticmethod
    async def read_subject(session: SessionDep, id: int):
        subject = await SubjectService.get_subject_by_id(session, id)
        if not subject:
            raise HTTPException(status_code= 404, detail="Subject not found")
        return {"message": "subject found", "ok": True, "data": subject}
    
    @staticmethod
    async def get_all_subjects_for_teacher(session: SessionDep, teacher_id: int):
        subjects = await SubjectService.get_all_subjects_for_teacher(session, teacher_id)
        if not subjects:
            raise HTTPException(status_code= 404, detail="Subjects not found")
        return {"message": "subjects found", "ok": True, "data": subjects}
    
    @staticmethod
    async def enrollment_class(session: SessionDep, enrollment: EnrollmentBase):
        enrollment_student = await SubjectService.get_enrollment(session, enrollment)
        if enrollment_student:
            raise HTTPException(status_code=400, detail="Enrollment already exists")
        enrollment_to_subject = await SubjectService.enrollment_to_subject(session, enrollment)
        return {"message": "enrollment success", "ok": True, "data": enrollment_to_subject}