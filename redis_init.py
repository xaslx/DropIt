import asyncio
from redis.asyncio import Redis as aioredis
from redis.exceptions import RedisError
from config import settings
from logger import logger

async def check_redis_connection(redis: aioredis) -> bool:
    try:
        await redis.ping()
        return True
    except RedisError:
        return False

async def init_redis() -> aioredis | None:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
        socket_timeout=1,
        socket_connect_timeout=1,
    )
    if await check_redis_connection(redis):
        return redis
    else:
        logger.error('Ошибка подключения к Redis')
        return None
