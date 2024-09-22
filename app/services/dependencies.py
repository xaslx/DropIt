from app.repositories.user import UserRepository
from app.services.user import UserService

from app.repositories.file import FileRepository
from app.services.file import FileService

from app.repositories.blacklist import BlackListRepository
from app.services.blacklist import BlackListService

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from fastapi import Depends
from redis.asyncio import Redis
from redis_init import init_redis



async def get_async_redis() -> Redis | None:
    return await init_redis()


def get_user_service(
        session: AsyncSession = Depends(get_async_session),
        redis: Redis | None = Depends(get_async_redis)
    ) -> UserService:

    repository = UserRepository(session=session)
    return UserService(repository=repository, redis=redis)


def get_file_service(
        session: AsyncSession = Depends(get_async_session),
        redis: Redis | None = Depends(get_async_redis)
    ) -> FileService:

    repository = FileRepository(session=session)
    return FileService(repository=repository, redis=redis)


def get_blacklist_service(session: AsyncSession = Depends(get_async_session)) -> BlackListService:
    repository = BlackListRepository(session=session)
    return BlackListService(repository=repository)