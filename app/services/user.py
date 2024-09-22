from app.repositories.user import UserRepository
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.schemas.user import UserOut
from logger import logger


class UserService:

    def __init__(self, repository: type[UserRepository], redis: Redis | None) -> None:
        self.repository = repository
        self.redis = redis

    async def create(self, ip_address: str) -> UserOut:
        return await self.repository.add(ip_address=ip_address)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)


    async def get_user(self, ip_address: str) -> None | UserOut:
        if self.redis:
            try:
                cached_data_user: None | str = await self.redis.get(ip_address)
                if cached_data_user:
                    return UserOut(id=int(cached_data_user), ip_address=ip_address)
            except RedisError:
                logger.error('Ошибка получения кэша')

        user: UserOut | None = await self.repository.find_one_or_none(ip_address=ip_address)

        if user and self.redis:
            try:
                await self.redis.set(ip_address, user.id, ex=86400)
            except RedisError:
                logger.error('Не удалось добавить пользователя в кэш')

        return user
 


