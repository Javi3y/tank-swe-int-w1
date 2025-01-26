from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import as_declarative
from .config import settings
from sqlalchemy.sql.functions import current_timestamp

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(
        "created_at", DateTime(), default=current_timestamp(), nullable=False
    )


async def get_db():
    async with SessionLocal() as db:
        yield db
