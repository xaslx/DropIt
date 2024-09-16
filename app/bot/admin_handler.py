from aiogram import Router
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.state import default_state
from aiogram.types import Message
from app.bot.admin_filter import AdminProtect
from app.bot.bot_service import BotService
import ipaddress
from app.schemas.blacklist import BlackList
from app.schemas.file import FileSchemaOut


admin_router: Router = Router()


@admin_router.message(StateFilter(default_state), AdminProtect(), Command('apanel'))
async def admins_panel(message: Message):
    await message.answer(
        'Команды администраторов:\n\n/ban_ip - добавить ip в чс\n/unban_ip - убрать ip из чс\n/delete_file - удалить файл'
    )


@admin_router.message(StateFilter(default_state), AdminProtect(), Command('ban_ip'))
async def ban_ip(message: Message, command: CommandObject):
    if not command.args:
        return await message.answer(f'Вы не ввели IP адресс')
    user: BlackList = await BotService.get_person(ip_address=command.args)
    try:
        ipaddress.ip_address(command.args)
    except ValueError:
        return await message.answer('Введен некорректный IP')
    else:
        if not user:
            await BotService.add_person_to_blacklist(ip_address=str(command.args))
            return await message.answer('Вы добавили пользователя в черный список.')
        return await message.answer('Пользователь уже в черном списке.')



@admin_router.message(StateFilter(default_state), AdminProtect(), Command('unban_ip'))
async def unban_ban_ip(message: Message, command: CommandObject):
    if not command.args:
        return await message.answer('Вы не ввели IP адресс')
    user: BlackList = await BotService.get_person(ip_address=command.args)
    if user:
        await BotService.delete_person_from_blacklist(ip_address=command.args)
        return await message.answer('Пользователь удален из черного списка.')
    return await message.answer('Пользователь не находится в черном списке.')


@admin_router.message(StateFilter(default_state), AdminProtect(), Command('delete_file'))
async def delete_file(message: Message, command: CommandObject):
    if not command.args:
        return await message.answer('Вы не ввели ID файла')
    if command.args.isdigit():
        file: FileSchemaOut = await BotService.get_file(file_id=command.args)
        if not file:
            return await message.answer('Файл не найден')
        await BotService.delete_file(file_id=file.id)
        return await message.answer(
            text=
            '❌ #файл_удален\n\n'
            f'Файл {file.id}, был удален администратором'
        )
    return await message.answer('File ID должен состоять только из цифр')

