from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.config import settings


# Creates the async database engine using the DATABASE_URL from our settings.
# The engine is the main connection point between SQLAlchemy and PostgreSQL.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)


# Creates a reusable factory for async database sessions.
# Each session represents a temporary conversation with the database.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# FastAPI dependency that gives each request its own database session.
# The session is automatically closed after the request finishes.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
