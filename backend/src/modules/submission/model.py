from sqlalchemy import (
    Enum,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base
from src.core.enum import FileTypeEnum


class Submission(Base):
    __tablename__ = "submission"

    __table_args__ = (UniqueConstraint("student_id", "assignment_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignment.id"), nullable=False
    )
    state_id: Mapped[int] = mapped_column(ForeignKey("type_state.id"), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=True)


class TypeState(Base):
    __tablename__ = "type_state"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    state: Mapped[str] = mapped_column(String, nullable=False)


class SubmissionFile(Base):
    __tablename__ = "submission_file"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submission.id"), nullable=False
    )
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    type_file: Mapped[FileTypeEnum] = mapped_column(Enum(FileTypeEnum), nullable=False)
