import os
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionFactory() as session:
        yield session

