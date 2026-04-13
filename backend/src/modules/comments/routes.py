from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile, status
from src.core.database import SessionDep
from src.core.enum import FileTypeEnum
from src.modules.comments.controllers import CommentController
from src.modules.comments.schemas import SubmissionCommentCreate, SubmissionCommentUpdate

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    session: SessionDep,
    id_submission: int,
    comment_data: SubmissionCommentCreate,
):
    return await CommentController.create_comment(
        session,
        id_submission,
        comment_data,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_comments(session: SessionDep, id_submission: int):
    return await CommentController.get_all_comments(session, id_submission)


@router.get(
    "/{id_comment}",
    status_code=status.HTTP_200_OK,
)
async def get_comment(
    session: SessionDep, id_submission: int, id_comment: int
):
    return await CommentController.get_comment(session, id_submission, id_comment)


@router.patch(
    "/{id_comment}",
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    session: SessionDep,
    id_submission: int,
    id_comment: int,
    comment_data: SubmissionCommentUpdate,
):
    return await CommentController.update_comment(
        session, id_submission, id_comment, comment_data
    )


@router.delete(
    "/{id_comment}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    session: SessionDep, id_submission: int, id_comment: int
):
    return await CommentController.delete_comment(session, id_submission, id_comment)


@router.post(
    "/{id_comment}/file",
    status_code=status.HTTP_201_CREATED,
)
async def add_file_to_comment(
    session: SessionDep,
    id_submission: int,
    id_comment: int,
    file_type: Annotated[FileTypeEnum, Form()],
    file: UploadFile = File(...),
):
    return await CommentController.add_file_to_comment(
        session, id_submission, id_comment, file, file_type
    )


@router.get(
    "/{id_comment}/file/{id_file}",
    status_code=status.HTTP_200_OK,
)
async def get_file_from_comment(
    session: SessionDep,
    id_submission: int,
    id_comment: int,
    id_file: int,
):
    return await CommentController.get_file_from_comment(
        session, id_submission, id_comment, id_file
    )


@router.get(
    "/{id_comment}/file/",
    status_code=status.HTTP_200_OK,
)
async def get_all_files_by_comment(
    session: SessionDep,
    id_submission: int,
    id_comment: int,
):
    return await CommentController.get_all_files_by_comment(
        session, id_submission, id_comment
    )
