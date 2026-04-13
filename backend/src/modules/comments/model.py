from datetime import datetime

from sqlalchemy import (
    DateTime,
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
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teacher.id"), nullable=False
    )
    comment: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


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
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
