from fastapi import HTTPException
from src.core.database import SessionDep
from src.modules.teacher.services import TeacherService


class TeacherController:
    @staticmethod
    async def get_teacher(session: SessionDep, id: int):
        teacher = await TeacherService.get_teacher_by_id(session, id)
        if not teacher:
            raise HTTPException(status_code=404, detail="teacher not found")
        return {"message": "teacher found", "ok": True, "data": teacher}
