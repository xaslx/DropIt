from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.file import File



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    cookie_uuid: Mapped[str] = mapped_column(unique=True)
    
    files: Mapped[list['File']] = relationship(back_populates='user')