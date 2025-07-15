from cache.redis_cache import redis_client
import redis.asyncio as redis
from cache.memory_cache import lru_cache 

async def start_redis_subscriber():

  pubsub = redis_client.pubsub()
  await pubsub.subscribe('lru_cache_validation')

  async for message in pubsub.listen():
    if message['type'] == "message":
      raw_data = message["data"].decode()
      doctor_id, date = raw_data.split("|")
      key = (doctor_id, date)
      lru_cache.remove(key)
   

