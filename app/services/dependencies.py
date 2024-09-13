from app.repositories.user import UserRepository
from app.services.user import UserService

from app.repositories.file import FileRepository
from app.services.file import FileService


def get_user_service():
    return UserService(UserRepository)


def get_file_service():
    return FileService(FileRepository)