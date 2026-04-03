from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.modules.profesion.model import Profesion
from src.modules.profesion.schemas import ProfesionCreate

async def get_profesion_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Profesion).where(Profesion.name == name))
    return result.scalar_one_or_none()

async def create_profesion(db: AsyncSession, data: ProfesionCreate):
    profesion = Profesion(**data.model_dump())
    db.add(profesion)
    await db.commit()
    await db.refresh(profesion)
    return profesion

async def get_all_profesiones(db: AsyncSession):
    result = await db.execute(select(Profesion))
    return result.scalars().all()

async def get_profesion_by_id(db: AsyncSession, profesion_id: int):
    result = await db.execute(select(Profesion).where(Profesion.id == profesion_id))
    return result.scalar_one_or_none()

async def delete_profesion(db: AsyncSession, profesion: Profesion):
    await db.delete(profesion)
    await db.commit()