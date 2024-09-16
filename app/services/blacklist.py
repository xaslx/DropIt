from app.repositories.blacklist import BlackListRepository
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.blacklist import BlackList


class BlackListService:

    def __init__(self, repository: type[BlackListRepository]) -> None:
        self.repository= repository()

    async def create(self, session: AsyncSession, ip_address: str) -> BlackList:
        return await self.repository.add(session=session, ip_address=ip_address)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, ip_address: str, session: AsyncSession) -> BlackList:
        return await self.repository.find_one_or_none(ip_address=ip_address, session=session)
 


