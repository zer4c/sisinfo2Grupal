from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile, status
from pydantic import Json
from src.core.database import SessionDep
from src.modules.submission.controllers import SubmissionController
from src.modules.submission.schemas import SubmissionBase, SubmissionFile

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_submission(session: SessionDep, submission_info: SubmissionBase):
    return await SubmissionController.create_submission(session, submission_info)


@router.get(
    "/{assignment_id}",
    status_code=status.HTTP_200_OK,
)
async def get_submissions_done(session: SessionDep, assignment_id: int):
    return await SubmissionController.get_submissions_done(session, assignment_id)


@router.post(
    "/{id_submission}/file",
    status_code=status.HTTP_200_OK,
)
async def create_file_submission(
    submission_data: Annotated[Json[SubmissionFile], Form()],
    session: SessionDep,
    data: UploadFile = File(...),
):
    return await SubmissionController.create_file_submission(
        session, submission_data, data
    )


@router.get(
    "/{id_submission}/file/{id_file}",
    status_code=status.HTTP_200_OK,
)
async def get_file_submission(session: SessionDep, id_file: int):
    return await SubmissionController.get_file_submission(session, id_file)


@router.get("/{id_submission}/file/", status_code=status.HTTP_200_OK)
async def get_all_file_by_submission(session: SessionDep, id_submission: int):
    return await SubmissionController.get_all_file_by_submission(session, id_submission)
