from src.core.database import SessionDep
from src.modules.student.services import StudentService
from fastapi import HTTPException
class StudentController:
    @staticmethod
    async def get_student(session : SessionDep , id : int):
        student = await StudentService.get_student_by_id(session, id)
        if not student:
            raise HTTPException(status_code = 404, detail="Student not found")
        return {"message": "Student found", "ok": True, "data": student} 
