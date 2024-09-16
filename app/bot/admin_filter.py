from aiogram.filters import Filter
from aiogram.types import Message

from config import settings


class AdminProtect(Filter):

    def __init__(self):
        self.admins: list[int] = settings.id_admins_telegram

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins