import redis.asyncio as aioredis
import os

REDIS_URL = os.getenv("REDIS_URL")

pool = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_redis():
    async with pool.client() as client:
        yield client