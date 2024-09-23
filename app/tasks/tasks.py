from app.utils.S3 import s3_client
from config import settings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties





bot: Bot = Bot(settings.bot_token_tg, default=DefaultBotProperties(parse_mode="HTML"))

async def delete_file_from_s3(filename: str):
    await s3_client.delete_file(object_name=filename)


async def send_report(file_id: int, file_url: str):
    await bot.send_message(
        chat_id=settings.id_admins_telegram,
        text=
        '❗️ #репорт\n\n'
        f'file_id: {file_id}\n\n'
        f'file_url: {file_url}'
    )


async def add_new_file(file_id: int, file_url: str):
    await bot.send_message(
        chat_id=settings.id_admins_telegram,
        text=
        '✅ #новый_файл\n\n'
        f'Добавлен новый файл\n\n'
        f'file_id: {file_id}\n\n'
        f'file_url: {file_url}'
    )


async def delete_file_admin(file_id: int):
    await bot.send_message(
        chat_id=settings.id_admins_telegram,
        text=
        f'❌ #файл_удален\n\n'
        f'Файл {file_id}, был удален администратором'
    )