import os
import json
from redis import asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis = aioredis.from_url(REDIS_URL, decode_responses=True)

DEFAULT_TTL = 300  # 5 minutes


async def get_cache(key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def set_cache(key: str, value, ttl: int = DEFAULT_TTL):
    await redis.set(key, json.dumps(value), ex=ttl)


async def delete_cache(key: str):
    await redis.delete(key)


async def delete_cache_pattern(pattern: str):
    keys = []
    async for key in redis.scan_iter(match=pattern):
        keys.append(key)
    if keys:
        await redis.delete(*keys)
