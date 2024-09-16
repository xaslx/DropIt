from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.blacklist import BlackList



class BlackListRepository(SQLAlchemyRepository):
    model: BlackList = BlackList