from app.repositories.user import UserRepository
from app.services.user import UserService

from app.repositories.file import FileRepository
from app.services.file import FileService

from app.repositories.blacklist import BlackListRepository
from app.services.blacklist import BlackListService

def get_user_service():
    return UserService(UserRepository)


def get_file_service():
    return FileService(FileRepository)


def get_blacklist_service():
    return BlackListService(BlackListRepository)