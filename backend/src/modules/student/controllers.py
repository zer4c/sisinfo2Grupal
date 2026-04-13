from fastapi import HTTPException
from src.core.database import SessionDep
from src.modules.student.services import StudentService


class StudentController:
    @staticmethod
    async def get_student(session: SessionDep, id: int):
        student = await StudentService.get_student_by_id(session, id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student found", "ok": True, "data": student}

    @staticmethod
    async def get_all_notification_by_student(session: SessionDep, id: int):
        student = await StudentService.get_student_by_id(session, id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        notifications = await StudentService.get_all_notification_by_student(session, id)
        return {"message": "Notifications found", "ok": True, "data": notifications}