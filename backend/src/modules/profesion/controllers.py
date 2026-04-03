from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.profesion.schemas import ProfesionCreate
from src.modules.profesion import services

async def create_profesion_controller(db: AsyncSession, data: ProfesionCreate):
    existing = await services.get_profesion_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=409, detail=f"Ya existe una profesión con el nombre '{data.name}'")
    return await services.create_profesion(db, data)

async def get_all_controller(db: AsyncSession):
    return await services.get_all_profesiones(db)

async def delete_profesion_controller(db: AsyncSession, profesion_id: int):
    profesion = await services.get_profesion_by_id(db, profesion_id)
    if not profesion:
        raise HTTPException(status_code=404, detail="Profesión no encontrada")
    return await services.delete_profesion(db, profesion)