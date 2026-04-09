from src.core.database import Base
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column


class Profesion(Base):
    __tablename__ = "profesiones"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    position: Mapped[int] = mapped_column(Numeric, nullable=False, unique=True)
    salary: Mapped[int] = mapped_column(Numeric, nullable=False)
