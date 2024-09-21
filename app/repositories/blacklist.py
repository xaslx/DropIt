from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.blacklist import BlackList



class BlackListRepository(SQLAlchemyRepository):
    model: BlackList = BlackList

    def __init__(self, session: AsyncSession):
        super().__init__(session)