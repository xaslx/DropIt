from app.repositories.blacklist import BlackListRepository


from app.schemas.blacklist import BlackList


class BlackListService:

    def __init__(self, repository: type[BlackListRepository]) -> None:
        self.repository= repository

    async def create(self, ip_address: str) -> BlackList:
        return await self.repository.add(ip_address=ip_address)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, ip_address: str) -> BlackList:
        return await self.repository.find_one_or_none(ip_address=ip_address)
 


