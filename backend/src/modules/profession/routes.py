from fastapi import APIRouter
from fastapi import status

from src.core.database import SessionDep
from src.modules.profession.schemas import ProfessionBase
from src.modules.profession.controllers import ProfessionControllers

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_profession(session: SessionDep, profession: ProfessionBase):
    return await ProfessionControllers.create_profession(session, profession)