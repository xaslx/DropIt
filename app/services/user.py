from app.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession



from app.repositories.base import AbstractRepository
from app.schemas.user import UserOut


class UserService:

    def __init__(self, repository: type[UserRepository]) -> None:
        self.repository= repository()

    async def create(self, session: AsyncSession, ip_address: str) -> UserOut:
        return await self.repository.add(session=session, ip_address=ip_address)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, session: AsyncSession, **filter_by) -> UserOut:
        return await self.repository.find_one_or_none(session=session, **filter_by)
 


