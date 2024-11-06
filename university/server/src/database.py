from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://admin:123@localhost:5432/univ"
SYNC_DATABASE_URL = "postgresql+psycopg2://admin:123@localhost:5432/univ"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
