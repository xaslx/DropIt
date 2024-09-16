from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from app.bot.admin_filter import AdminProtect


admin_router: Router = Router()


@admin_router.message(StateFilter(default_state), AdminProtect(), Command("apanel"))
async def admins_panel(message: Message):
    await message.answer(
        "Команды администраторов:\n\n/ban_ip - добавить ip в чс\n/unban_ip - убрать ip из чс\n/delete_file - удалить файл"
    )


