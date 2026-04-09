from src.core.database import SessionDep

from src.modules.subject.model import Subject
from src.modules.subject.schemas import (
    SubjectBase, 
    SubjectResponse
)


class SubjectService():
    @staticmethod
    async def create_subject(session: SessionDep, subject_info: SubjectBase):
        try:
            new_subject = Subject(
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
