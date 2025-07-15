# Handles cache invalidation when appointment is booked/cancelled. Can use Redis Pub/Sub or directly delete from both caches.

from cache.memory_cache import lru_cache 
from cache.redis_cache import delete as redis_delete
from cache.redis_cache import redis_client

async def invalidateCache(self, doctor_id, date):
    channel = 'lru_cache_validation'
    key = (doctor_id, str(date))
    lru_cache.remove(key)
    await redis_delete(key)
    await redis_client.publish(channel, f"{doctor_id}|{date}")


