from datetime import date

from sqlalchemy import select
from src.core.database import SessionDep
from src.modules.assignment.model import Assignment, AssignmentFile
from src.modules.assignment.schemas import (
    AssignmentBase,
    AssignmentFileCreate,
    AssignmentFileResponse,
    AssignmentResponse,
)
from src.modules.subject.model import Enrollment, Subject


class AssignmentService:
    @staticmethod
    async def get_by_title_and_subject(
        session: SessionDep, title: str, subject_id: int
    ):
        try:
            result = await session.execute(
                select(Assignment).where(
                    Assignment.title == title, Assignment.subject_id == subject_id
                )
            )
            assignment_orm = result.scalars().one_or_none()
            if not assignment_orm:
                return None
            return AssignmentResponse.model_validate(assignment_orm)
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
                points=assignment_info.points,
            )
            session.add(new_assignment)
            await session.commit()
            await session.refresh(new_assignment)
            return AssignmentResponse.model_validate(new_assignment)
        except Exception:
            session.rollback()
            raise

    @staticmethod
    async def get_assignment_by_id(session: SessionDep, assignment_id: int):
        try:
            result = await session.execute(
                select(Assignment).where(Assignment.id == assignment_id)
            )
            assignment_orm = result.scalars().one_or_none()
            if not assignment_orm:
                return None
            return AssignmentResponse.model_validate(assignment_orm)
        except Exception:
            raise

    @staticmethod
    async def get_all_assignments_for_subject(session: SessionDep, subject_id: int):
        try:
            result = await session.execute(
                select(Assignment).where(Assignment.subject_id == subject_id)
            )
            assignments_orm = result.scalars().all()
            if not assignments_orm:
                return None
            return [AssignmentResponse.model_validate(a) for a in assignments_orm]
        except Exception:
            raise

    @staticmethod
    async def get_assignments_for_student(
        session: SessionDep, subject_id: int, student_id: int
    ):
        try:
            subject_result = await session.execute(
                select(Subject).where(Subject.id == subject_id)
            )
            subject_orm = subject_result.scalars().one_or_none()
            if not subject_orm:
                return "subject not found"

            enrollment_result = await session.execute(
                select(Enrollment).where(
                    Enrollment.id_student == student_id,
                    Enrollment.id_subject == subject_id,
                )
            )
            if not enrollment_result.scalars().first():
                return "student not enrolled in subject"

            result = await session.execute(
                select(Assignment).where(Assignment.subject_id == subject_id)
            )
            assignments_orm = result.scalars().all()
            if not assignments_orm:
                return None
            return [AssignmentResponse.model_validate(a) for a in assignments_orm]
        except Exception:
            raise

    @staticmethod
    async def create_file_assignment(session: SessionDep, assignment_file_data):
        try:
            new_file = AssignmentFile(
                assignment_id=assignment_file_data.assignment_id,
                type_file=assignment_file_data.type_file,
                data=assignment_file_data.data,
            )
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
            return AssignmentFileResponse.model_validate(new_file)
        except Exception:
            session.rollback()
            raise

    @staticmethod
    async def get_file_assignment(session: SessionDep, id_file: int):
        try:
            result = await session.execute(
                select(AssignmentFile).where(AssignmentFile.id == id_file)
            )
            file_orm = result.scalars().one_or_none()
            if not file_orm:
                return None
            return AssignmentFileCreate.model_validate(file_orm)
        except Exception:
            raise

    @staticmethod
    async def get_all_file_by_assignment(session: SessionDep, id_assignment: int):
        try:
            result = await session.execute(
                select(AssignmentFile).where(
                    AssignmentFile.assignment_id == id_assignment
                )
            )
            files_orm = result.scalars().all()
            return [AssignmentFileResponse.model_validate(f) for f in files_orm]
        except Exception:
            raise
