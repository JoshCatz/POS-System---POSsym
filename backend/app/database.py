from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
