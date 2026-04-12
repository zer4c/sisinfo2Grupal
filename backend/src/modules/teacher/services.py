from src.core.database import SessionDep
from src.modules.teacher.model import Teacher
from src.modules.teacher.schemas import TeacherResponse
from sqlalchemy import select


class teacherService:
    @staticmethod
    async def get_teacher_by_id(session: SessionDep, id: int):
        try:
            teacher = await session.execute(select(Teacher).where(Teacher.id == id))
            teacher_orm = teacher.scalars().one_or_none()
            if not teacher_orm:
                return None
            return TeacherResponse.model_validate(teacher_orm)
        except Exception:
            raise
