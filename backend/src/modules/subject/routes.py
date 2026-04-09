from src.core.database import Base
from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code : Mapped[str] = mapped_column(ForeignKey("subjects.code"), nullable=False)
    period: Mapped[date] = mapped_column(ForeignKey("subjects.period"), nullable=False)
    teacher_id : Mapped[int] = mapped_column(ForeignKey("subjects.teacher_id"), nullable=False)
    student_id : Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)



class Subject(Base):
    __tablename__ = "subjects"
    code: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    period: Mapped[date] = mapped_column(Date, primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    max_students:  Mapped[int] = mapped_column(Integer, nullable=False)
    
    teacher : Mapped["Teacher"] = relationship("src.modules.teacher.model.Teacher", back_populates="subject")