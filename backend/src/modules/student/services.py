from sqlalchemy import select
from src.core.database import SessionDep
from src.modules.student.model import Student
from src.modules.student.schemas import StudentResponse, NotificationResponse
from src.modules.comments.model import Notification


class StudentService:
    @staticmethod
    async def get_student_by_id(session: SessionDep, id: int):
        try:
            student = await session.execute(select(Student).where(Student.id == id))
            student_orm = student.scalars().one_or_none()
            if not student_orm:
                return None
            return StudentResponse.model_validate(student_orm)
        except Exception:
            raise

    @staticmethod
    async def get_all_notification_by_student(session: SessionDep, id: int):
        try:
            result = await session.execute(
                select(Notification).where(Notification.id == id)
            )
            result_orm = result.scalars().all()
            return [
                NotificationResponse.model_validate(notification)
                for notification in result_orm
            ]
        except Exception:
            raise
