
import redis.asyncio as redis
from app.config import get_settings

settings = get_settings()

class RedisClient:
    def __init__(self):
        self.redis_url = settings.redis_url
        self.client = None

    async def connect(self):
        if not self.client:
            self.client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def get(self, key: str):
        if not self.client:
            await self.connect()
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        if not self.client:
            await self.connect()
        return await self.client.set(key, value, ex=expire)
        
    async def delete(self, key: str):
        if not self.client:
            await self.connect()
        return await self.client.delete(key)
        
    async def publish(self, channel: str, message: str):
        if not self.client:
            await self.connect()
        return await self.client.publish(channel, message)

    async def subscribe(self, channel: str):
        if not self.client:
            await self.connect()
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

redis_client = RedisClient()

async def get_redis() -> RedisClient:
    if not redis_client.client:
        await redis_client.connect()
    return redis_client
