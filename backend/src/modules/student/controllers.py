from fastapi import HTTPException
from src.core.database import SessionDep
from .services import StudentService
from .schemas import StudentCreate, StudentUpdate

class StudentController:
    @staticmethod
    async def get_all(session: SessionDep):
        return await StudentService.get_all(session)

    @staticmethod
    async def get_by_id(session: SessionDep, student_id: int):
        student = await StudentService.get_by_id(session, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    @staticmethod
    async def create(session: SessionDep, data: StudentCreate):
        student = await StudentService.create(session, data)
        return {"message": "student created", "ok": True, "data": student}

    @staticmethod
    async def update(session: SessionDep, student_id: int, data: StudentUpdate):
        updated_student = await StudentService.update(session, student_id, data)
        if not updated_student:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {"message": "student updated", "ok": True, "data": updated_student}

    @staticmethod
    async def delete(session: SessionDep, student_id: int):
        deleted = await StudentService.delete(session, student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {"message": "student deleted", "ok": True}