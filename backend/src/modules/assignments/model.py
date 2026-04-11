from src.core.database import Base
from sqlalchemy import (
    String,
    Date,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Assignment(Base):
    __tablename__ = "assignments"

    id_assignment: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_subject: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)