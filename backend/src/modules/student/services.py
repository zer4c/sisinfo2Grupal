from sqlalchemy import select
from src.core.database import SessionDep
from .model import Student
from .schemas import StudentCreate, StudentUpdate, StudentResponse

class StudentService():
    @staticmethod
    async def get_all(session: SessionDep):
        try:
            result = await session.execute(
                select(Student).order_by(Student.id.asc())
            )
            students = result.scalars().all()
            return [StudentResponse.model_validate(s) for s in students]
        except Exception:
            raise

    @staticmethod
    async def get_by_id(session: SessionDep, student_id: int):
        try:
            result = await session.execute(
                select(Student).where(Student.id == student_id)
            )
            student_orm = result.scalars().one_or_none()
            if not student_orm:
                return None
            return StudentResponse.model_validate(student_orm)
        except Exception:
            raise

    @staticmethod
    async def create(session: SessionDep, student_info: StudentCreate):
        try:
            new_student = Student(name=student_info.name, age=student_info.age)
            session.add(new_student)
            await session.commit()
            await session.refresh(new_student)
            return StudentResponse.model_validate(new_student)
        except Exception:
            raise

    @staticmethod
    async def update(session: SessionDep, student_id: int, student_info: StudentUpdate):
        try:
            result = await session.execute(
                select(Student).where(Student.id == student_id)
            )
            student_orm = result.scalars().one_or_none()
            if not student_orm:
                return None
            
            update_data = student_info.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(student_orm, key, value)
                
            await session.commit()
            await session.refresh(student_orm)
            return StudentResponse.model_validate(student_orm)
        except Exception:
            raise

    @staticmethod
    async def delete(session: SessionDep, student_id: int):
        try:
            result = await session.execute(
                select(Student).where(Student.id == student_id)
            )
            student_orm = result.scalars().one_or_none()
            if not student_orm:
                return False
                
            await session.delete(student_orm)
            await session.commit()
            return True
        except Exception:
            raise