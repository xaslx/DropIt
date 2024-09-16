from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class BlackList(Base):
    __tablename__ = 'blacklist'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(unique=True)