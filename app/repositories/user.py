from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.user import User



class UserRepository(SQLAlchemyRepository):
    model: User = User