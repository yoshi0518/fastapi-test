from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import config

DATABASE_URL = f"postgresql+asyncpg://{config.neon_user}:{config.neon_password}@{config.neon_host}/{config.neon_db}"

engine = create_async_engine(DATABASE_URL, echo=config.debug)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
metadata = MetaData()


async def get_db():
    async with async_session() as session:
        yield session
