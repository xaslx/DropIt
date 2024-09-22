from redis.asyncio import Redis as aioredis
from redis import Redis
from redis.exceptions import RedisError
from config import settings
from logger import logger


# redis: Redis = aioredis.from_url(
#     f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
#     encoding="utf-8",
#     decode_responses=True,
# )

redis = None
async def init_redis() -> aioredis | None:
    try:
        return aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=1,
            socket_connect_timeout=1,
        )
    except RedisError:
        logger.error('Ошибка подключения к Redis')
        return None