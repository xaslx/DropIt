from app.repositories.sqlalchemy import SQLAlchemyRepository
from app.models.file import File



class FileRepository(SQLAlchemyRepository):
    model: File = File