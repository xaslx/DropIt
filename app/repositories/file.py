from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.file import File
from sqlalchemy import select, desc, func
from app.schemas.file import FileSchemaOut
from logger import logger
from sqlalchemy.exc import SQLAlchemyError
import asyncio
from app.tasks.tasks import new_error

class FileRepository(SQLAlchemyRepository):
    model: File = File

    def __init__(self, session: AsyncSession):
        super().__init__(session)


    async def find_all(self, user_id: int, limit: int = 15, offset: int = 0):
        try:
            stmt_data = (
                select(self.model.__table__.columns)
                .where(self.model.user_id == user_id)
                .order_by(desc(self.model.id))
                .offset(offset)
                .limit(limit)
            )
            res_data = await self.session.execute(stmt_data)
            user_files: FileSchemaOut = res_data.mappings().all()

            stmt_count = (
                select(func.count())
                .where(self.model.user_id == user_id)
            )
            res_count = await self.session.execute(stmt_count)
            total_count: int = res_count.scalar()

            return user_files, total_count
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка, при поиске файла: {e}')
            asyncio.create_task(new_error(text=f'Ошибка при получении файла, "ошибка": {e}'))
            raise e