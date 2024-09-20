from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.file import File
from sqlalchemy import select, desc, func
from app.models.user import User
from app.schemas.file import FileSchemaOut

class FileRepository(SQLAlchemyRepository):
    model: File = File


    async def find_all(self, session: AsyncSession, user_id: int, limit: int = 15, offset: int = 0):
        stmt_data = (
            select(self.model.__table__.columns)
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.id))
            .offset(offset)
            .limit(limit)
        )
        res_data = await session.execute(stmt_data)
        user_files: FileSchemaOut = res_data.mappings().all()

        stmt_count = (
            select(func.count())
            .where(self.model.user_id == user_id)
        )
        res_count = await session.execute(stmt_count)
        total_count: int = res_count.scalar()

        return user_files, total_count