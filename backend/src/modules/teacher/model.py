from src.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
