from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.profesion.services import ProfesionService
from src.modules.profesion.schemas import ProfesionCreate


class ProfesionController:
    @staticmethod
    async def register(session: AsyncSession, profession: ProfesionCreate) -> dict:
        if await ProfesionService.get_by_name(session, profession.name):
            raise HTTPException(
                status_code=400,
                detail="The profession already exists.",
            )
        if await ProfesionService.get_by_position(session, profession.position):
            raise HTTPException(
                status_code=400,
                detail="The position is already in use.",
            )
        return await ProfesionService.register(session, profession)
