from sqlalchemy import delete, insert, select
from database import async_session_maker
from app.models.blacklist import BlackList
from database import async_session_maker
from app.models.file import File
from logger import logger
from sqlalchemy.exc import SQLAlchemyError



class BotService:
    model: BlackList = BlackList

    @classmethod
    async def get_person(cls, ip_address: str):
        async with async_session_maker() as session:
            try:
                stmt = select(cls.model.__table__.columns).filter_by(ip_address=ip_address)
                res = await session.execute(stmt)
                return res.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    'Ошибка при получении записи с базы данных', extra={'данные': ip_address, 'ошибка': e}
                )


    @classmethod
    async def add_person_to_blacklist(cls, ip_address: str):
        async with async_session_maker() as session:
            try:
                stmt = insert(cls.model).values(ip_address=ip_address)
                await session.execute(stmt)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    'Ошибка при добавлении записи в базу данных', extra={'данные': ip_address, 'ошибка': e}
                )


    @classmethod
    async def delete_person_from_blacklist(cls, ip_address: str):
        async with async_session_maker() as session:
            try:
                stmt = delete(cls.model).filter_by(ip_address=ip_address)
                await session.execute(stmt)
                await session.commit()     
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    'Ошибка при удалении записи с базы данных', extra={'данные': ip_address, 'ошибка': e}
                )


    @classmethod
    async def get_file(cls, file_id: int):
        async with async_session_maker() as session:
            try:
                stmt = select(File).filter_by(id=int(file_id))
                res = await session.execute(stmt)
                return res.scalar_one_or_none()  
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    'Ошибка при получении записи c базы данных', extra={'данные': file_id, 'ошибка': e}
                )


    @classmethod
    async def delete_file(cls, file_id: int):
        async with async_session_maker() as session:
            try:
                stmt = delete(File).filter_by(id=int(file_id))
                await session.execute(stmt)
                await session.commit()    
            except (SQLAlchemyError, Exception) as e:
                logger.error(
                    'Ошибка при удалении записи с базы данных', extra={'данные': file_id, 'ошибка': e}
                )