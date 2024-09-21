from app.repositories.user import UserRepository
from app.services.user import UserService

from app.repositories.file import FileRepository
from app.services.file import FileService

from app.repositories.blacklist import BlackListRepository
from app.services.blacklist import BlackListService

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from fastapi import Depends


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    repository = UserRepository(session=session)
    return UserService(repository=repository)


def get_file_service(session: AsyncSession = Depends(get_async_session)) -> FileService:
    repository = FileRepository(session=session)
    return FileService(repository=repository)


def get_blacklist_service(session: AsyncSession = Depends(get_async_session)) -> BlackListService:
    repository = BlackListRepository(session=session)
    return BlackListService(repository=repository)