from sqlalchemy import select
from src.core.database import SessionDep

from src.modules.subject.model import Subject
from src.modules.subject.schemas import (
    SubjectBase, 
    SubjectResponse
)


class SubjectService():
    @staticmethod
    async def get_subject_by_name(session: SessionDep, subject_name: str):
        try:
            subject = await session.execute(
                select(Subject).
                where(Subject.name == subject_name)
            )
            subject_orm = subject.scalars().one_or_none()
            if not subject_orm:
                return None
            return SubjectResponse.model_validate(subject_orm)
        except Exception:
            raise
        
    @staticmethod
    async def create_subject(session: SessionDep, subject_info: SubjectBase):
        try:
            new_subject = Subject(
                code = subject_info.code,
                period = subject_info.period,
                teacher_id = subject_info.teacher_id,
                name = subject_info.name,
                description = subject_info.description,
                max_students = subject_info.max_students
            )
            session.add(new_subject)
            await session.commit()
            await session.refresh(new_subject)
            return SubjectResponse.model_validate(new_subject)
        except Exception:
            await session.rollback()
            raise
