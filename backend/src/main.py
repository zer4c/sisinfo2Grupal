import logging
from contextlib import asynccontextmanager

import src.core.mapping_database  # noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from src.core import api
from src.core.config import config
from src.core.database import create_db_and_tables, engine

logger = logging.getLogger("uvicorn.info")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await create_db_and_tables()
            logger.info(f"Database connection successful: {config.db_name}")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    yield


app = FastAPI(title=config.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")
