from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from app.models.user import User


class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    url: Mapped[str] = mapped_column(unique=True)
    filename: Mapped[str]
    upload_date: Mapped[DateTime] = mapped_column(DateTime)
    content_type: Mapped[str]

    user: Mapped['User'] = relationship(back_populates='files')