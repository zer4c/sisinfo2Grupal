from fastapi import APIRouter
from src.core.database import SessionDep
from src.modules.profesion.schemas import ProfesionCreate, ProfesionResponse
from src.modules.profesion import controllers

router = APIRouter(prefix="/profesiones", tags=["Profesiones"])

@router.post("/", response_model=ProfesionResponse, status_code=201)
async def create(data: ProfesionCreate, db: SessionDep):
    return await controllers.create_profesion_controller(db, data)

@router.get("/", response_model=list[ProfesionResponse])
async def get_all(db: SessionDep):
    return await controllers.get_all_controller(db)
    
@router.delete("/{profesion_id}", status_code=204)
async def delete(profesion_id: int, db: SessionDep):
    return await controllers.delete_profesion_controller(db, profesion_id)