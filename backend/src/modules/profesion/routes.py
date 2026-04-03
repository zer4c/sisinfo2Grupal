from fastapi import APIRouter

from src.core.database import SessionDep
from src.modules.profesion.controllers import ProfesionController
from src.modules.profesion.schemas import ProfesionCreate

router = APIRouter()


@router.post("/")
async def register_profession(profession: ProfesionCreate, session: SessionDep):
    return await ProfesionController.register(session, profession)
