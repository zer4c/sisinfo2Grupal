from datetime import date

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    LargeBinary,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base
from src.core.enum import FileTypeEnum


class SubmissionComment(Base):
    __tablename__ = "submission_comment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submission.id"), nullable=False
    )
    comment: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)


class CommentFile(Base):
    __tablename__ = "comment_file"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("submission_comment.id"), nullable=False
    )
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    type_file: Mapped[FileTypeEnum] = mapped_column(Enum(FileTypeEnum), nullable=False)


class Notification(Base):
    __tablename__ = "notification"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submission.id"), nullable=False
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("submission_comment.id"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)
