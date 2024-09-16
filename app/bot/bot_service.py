from sqlalchemy import delete, insert, select
from database import async_session_maker
from app.models.blacklist import BlackList
from database import async_session_maker
from app.services.dependencies import get_file_service


file_service = get_file_service()

class BotService:
    model: BlackList = BlackList

    @classmethod
    async def get_person(cls, ip_address: str):
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(ip_address=ip_address)
            res = await session.execute(stmt)
            return res.mappings().one_or_none()
    
    @classmethod
    async def add_person_to_blacklist(cls, ip_address: str):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(ip_address=ip_address)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_person_from_blacklist(cls, ip_address: str):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(ip_address=ip_address)
            await session.execute(stmt)
            await session.commit()     

    @classmethod
    async def get_file(cls, file_id: int):
        async with async_session_maker() as session:
            file = await file_service.get_one(session=session, id=int(file_id))
            return file

    @classmethod
    async def delete_file(cls, file_id: int):
        async with async_session_maker() as session:
            await file_service.delete(id=file_id, session=session)
