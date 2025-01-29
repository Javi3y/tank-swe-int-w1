from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import as_declarative
from .config import settings
from sqlalchemy.sql.functions import current_timestamp
import redis.asyncio as redis

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



class Redis:
    redis_client: redis.Redis| None = None

    @classmethod
    async def connect(
        cls, host: str = settings.redis_host, port: int = settings.redis_port, username=settings.redis_username, password=settings.redis_password
    ):
        try:
            cls.redis_client = redis.Redis(
                host=host, port=port, username=username, password=password
            )
        except redis.RedisError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

        await cls.redis_client

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            await cls.redis_client.aclose()

    @classmethod
    async def insert_string(cls, key: str, value: str, expiry_seconds: int|None = None):
        if expiry_seconds:
            await cls.redis_client.setex(key, expiry_seconds, value)
        else:
            await cls.redis_client.set(key, value)

    @classmethod
    async def query_key(cls, key: str):
        value = await cls.redis_client.get(key)
        if value == None:
            return None
        value = value.decode('utf-8')
        return value
