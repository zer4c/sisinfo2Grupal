from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.profesion.model import Profesion
from src.modules.profesion.schemas import ProfesionCreate


class ProfesionService:
    @staticmethod
    async def get_by_name(session: AsyncSession, name: str) -> Profesion | None:
        result = await session.execute(select(Profesion).where(Profesion.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_position(session: AsyncSession, position: int) -> Profesion | None:
        result = await session.execute(
            select(Profesion).where(Profesion.position == position)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def register(session: AsyncSession, profession: ProfesionCreate) -> dict:
        try:
            new_profession = Profesion(
                name=profession.name,
                position=profession.position,
                salary=profession.salary,
            )
            session.add(new_profession)
            await session.commit()
            await session.refresh(new_profession)
            return {
                "message": "Registration completed.",
                "ok": True,
                "data": {
                    "id": new_profession.id,
                    "name": new_profession.name,
                    "position": new_profession.position,
                    "salary": float(new_profession.salary),
                },
            }
        except Exception:
            await session.rollback()
            raise
