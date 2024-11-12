from app.repositories.user import UserRepository
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.schemas.user import UserOut
from logger import logger
import asyncio
from app.tasks.tasks import new_error




class UserService:

    def __init__(self, repository: type[UserRepository], redis: Redis | None) -> None:
        self.repository = repository
        self.redis = redis

    async def create(self, cookie_uuid: str) -> UserOut:
        return await self.repository.add(cookie_uuid=cookie_uuid)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)


    async def get_user(self, cookie_uuid: str) -> None | UserOut:
        if self.redis:
            try:
                cached_data_user: None | str = await self.redis.get(cookie_uuid)
                if cached_data_user:
                    return UserOut(id=int(cached_data_user), cookie_uuid=cookie_uuid)
            except RedisError:
                logger.error('Ошибка получения кэша')
                asyncio.create_task(new_error(text='Ошибка получения кэша'))

        user: UserOut | None = await self.repository.find_one_or_none(cookie_uuid=cookie_uuid)
        if user and self.redis:
            try:
                await self.redis.set(cookie_uuid, user.id, ex=86400)
            except RedisError:
                logger.error('Не удалось добавить пользователя в кэш')
                asyncio.create_task(new_error(text='Не удалось добавить пользователя в кэш'))

        return user
 


