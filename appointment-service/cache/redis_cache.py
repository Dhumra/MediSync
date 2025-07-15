# Async Redis cache for shared state across service instances. Provides get, set, delete.

import redis.asyncio as redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  # 5 minutes default

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def get(key):
    return await redis_client.get(key)

async def set(key, value):
    await redis_client.set(key, value, ex=CACHE_TTL)

async def delete(key):
    await redis_client.delete(key)
