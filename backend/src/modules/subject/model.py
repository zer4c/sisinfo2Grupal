from src.core.database import Base
from sqlalchemy import (
    String,
    Date,
    ForeignKey,
    Integer,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


class Enrollment(Base):
    __tablename__ = "enrollments"

    __table_args__ = (
        ForeignKeyConstraint(
            ["code", "period", "teacher_id"],
            ["subjects.code", "subjects.period", "subjects.teacher_id"],
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    __table_args__ = (UniqueConstraint("code", "period"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, index=True)
    period: Mapped[date] = mapped_column(Date, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    max_students: Mapped[int] = mapped_column(Integer, nullable=False)

    teacher: Mapped["Teacher"] = relationship(
        "src.modules.database.teacher.Teacher", back_populates="subject"
    )
