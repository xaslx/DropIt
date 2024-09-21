from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.user import User



class UserRepository(SQLAlchemyRepository):
    model: User = User


    def __init__(self, session: AsyncSession):
        super().__init__(session)