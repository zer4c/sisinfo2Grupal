from sqlalchemy import select
from src.core.database import SessionDep
from src.modules.profession.model import Profesion
from src.modules.profession.schemas import ProfessionBase
from src.modules.profession.schemas import ProfessionResponse


class ProfessionServices:
    @staticmethod
    async def get_profession(session: SessionDep, profession: ProfessionBase):
        try:
            result = session.execute(
                select(Profesion).where(Profesion.name == profession.name)
            )
            result_orm = result.scalars().one_or_none()
            return ProfessionResponse.model_validate(result_orm) if result_orm else None
        except Exception:
            raise

    @staticmethod
    async def create_profession(session: SessionDep, profession: ProfessionBase):
        try:
            new_profession = Profesion(
                name=profession.name,
                position=profession.position,
                salary=profession.salary
            )
            session.add(new_profession)
            session.commit()
            session.refresh(new_profession)
            return ProfessionResponse.model_validate(new_profession)
        except Exception:
            session.rollback()
            raise