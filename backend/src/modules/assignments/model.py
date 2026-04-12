from src.core.database import Base
from sqlalchemy import (
    String,
    Date,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Submission(Base):
    __tablename__ = "submissions"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"), primary_key=True)
    state: Mapped[str] = mapped_column(String, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=True)

class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)