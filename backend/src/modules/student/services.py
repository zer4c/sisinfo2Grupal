from src.core.database import SessionDep
from src.modules.student.model import Student
from src.modules.student.schemas import StudentResponse
from sqlalchemy import select
class StudentService:
    @staticmethod
    async def get_student(session : SessionDep, id : int):
        try:
            student = await session.execute(
                select(Student).
                where(Student.id == id)
            )
            student_orm = student.scalars().one_or_none()
            if not student_orm:
                return None
            return StudentResponse.model_validate(student_orm)
        except Exception:
            raise
    