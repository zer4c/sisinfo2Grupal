from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.core.database import SessionDep
from src.modules.profession.schemas import ProfessionBase
from src.modules.profession.services import ProfessionServices

class ProfessionControllers:
    @staticmethod
    async def create_profession(session: SessionDep, profession: ProfessionBase):
        profession_already= ProfessionServices.get_profession(session, profession)
        if profession_already:
            raise HTTPException(message="Profession already exists", ok=False)
        response = ProfessionServices.create_profession(session, profession)
        return JSONResponse(
            status_code=201,
            content={"message": "Profession created", "ok":True, "data": response}
        )