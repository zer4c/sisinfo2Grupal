from src.core.database import Base
from src.core.enum import FileTypeEnum
from sqlalchemy import (
    String,
    Date,
    ForeignKey,
    Integer,
    LargeBinary,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Assignment(Base):
    __tablename__ = "assignment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)


class AssignmentFile(Base):
    __tablename__ = "assignment_file"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignment.id"), nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    type_file: Mapped[FileTypeEnum] = mapped_column(Enum(FileTypeEnum), nullable=False)

class SubmissionComment(Base):
    __tablename__ = "submission_comment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submission.id"), nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)


class CommentFile(Base):
    __tablename__ = "comment_file"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("submission_comment.id"), nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    type_file: Mapped[FileTypeEnum] = mapped_column(Enum(FileTypeEnum), nullable=False)

class Notification(Base):
    __tablename__ = "notification"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignment.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)

