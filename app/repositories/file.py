from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.file import File
from sqlalchemy import select, desc, asc, func


class FileRepository(SQLAlchemyRepository):
    model: File = File


    async def find_all(self, session: AsyncSession, limit: int = 5, offset: int = 0, **filter_by):
        stmt = select(
            self.model.__table__.columns,
            func.count().over().label('total_count')
        ).filter_by(**filter_by).order_by(desc(self.model.id)).offset(offset).limit(limit)

        res = await session.execute(stmt)
        records = res.mappings().all()
        
        total_count = records[0]['total_count'] if records else 0
        
        return records, total_count