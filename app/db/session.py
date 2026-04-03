from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import settings


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

from sqlmodel import SQLModel
from app.config.config import settings

# ... (keep engine and sessionmaker as is)

async def init_db():
    from app.model import User, Organization, Workspace, Project, ProjectMember
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
