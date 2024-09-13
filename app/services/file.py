from app.repositories.file import FileRepository


from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.file import FileSchema


class FileService:

    def __init__(self, repository: type[FileRepository]) -> None:
        self.repository= repository()

    async def create(self, session: AsyncSession, **data) -> FileSchema:
        return await self.repository.add(session=session, **data)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, ip_address: str, session: AsyncSession) -> FileSchema:
        return await self.repository.find_one_or_none(ip_address=ip_address, session=session)

    async def get_all(self, session: AsyncSession, **data) -> list[FileSchema]:
        return await self.repository.find_all(session=session, **data)


