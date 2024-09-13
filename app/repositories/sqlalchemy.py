from app.repositories.base import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select



class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def add(self, session: AsyncSession, **data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.__table__.columns)
        res = await session.execute(stmt)
        await session.commit()
        return res.mappings().one_or_none()

    async def find_one_or_none(self, session: AsyncSession, **filter_by):
        stmt = select(self.model.__table__.columns).filter_by(**filter_by)
        res = await session.execute(stmt)
        return res.mappings().one_or_none()

    async def find_all(self, session: AsyncSession, **filter_by):
        stmt = select(self.model.__table__.columns).filter_by(**filter_by)
        res = await session.execute(stmt)
        return res.mappings().all()

    async def delete(self, session: AsyncSession, id: int) -> int:
        stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
        await session.execute(stmt)
        await session.commit()