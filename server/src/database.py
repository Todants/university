from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()

SYNC_DATABASE_URL = "postgresql+psycopg2://admin:123@localhost:5432/univ"
ASYNC_DATABASE_URL = "postgresql+asyncpg://admin:123@localhost:5432/univ"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


def get_sync_db():
    with SyncSessionLocal() as session:
        yield session


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
