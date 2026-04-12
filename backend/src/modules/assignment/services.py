from datetime import date
from sqlalchemy import select
from src.core.database import SessionDep

from src.modules.assignment.model import Assignment
from src.modules.assignment.schemas import (
    AssignmentBase, 
    AssignmentResponse,
)
class AssignmentService():
    @staticmethod
    async def get_by_title_and_subject(session: SessionDep, title: str, subject_id: int):
        try:
            result = await session.execute(
                select(Assignment).where(
                    Assignment.title == title,
                    Assignment.subject_id == subject_id
                )
            )
            assignment_orm = result.scalars().one_or_none()
            if not assignment_orm:
                return None
            return AssignmentResponse.model_validate(assignment_orm)
        except Exception:
            raise

    @staticmethod
    async def get_all_assignment_for_subject(session: SessionDep, id_subject: int):
        try:
            result = await session.execute(
                select(Assignment).
                where(Assignment.subject_id == id_subject).
                order_by(Assignment.created_at.desc())
            )
            assignment_orm = result.scalars().all()
            if not assignment_orm:
                return None
            return [AssignmentResponse.model_validate(a) for a in assignment_orm]
        except Exception:
            raise

    @staticmethod
    async def create_assignment(session: SessionDep, assignment_info: AssignmentBase):
        try:
            new_assignment = Assignment(
                subject_id=assignment_info.subject_id,
                title=assignment_info.title,
                description=assignment_info.description,
                created_at=date.today(),
                due_date=assignment_info.due_date,
                points=assignment_info.points
            )
            session.add(new_assignment)
            await session.commit()
            await session.refresh(new_assignment)
            return AssignmentResponse.model_validate(new_assignment)
        except Exception:
            raise