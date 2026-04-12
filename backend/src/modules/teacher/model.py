from src.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Teacher(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    subject: Mapped[List["Subject"]] = relationship(
        "src.modules.subject.model.Subject", back_populates="teacher"
    )