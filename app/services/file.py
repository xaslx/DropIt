from app.repositories.file import FileRepository


from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.file import FileSchema


class FileService:

    def __init__(self, repository: type[FileRepository]) -> None:
        self.repository= repository()

    async def create(self, session: AsyncSession, **data) -> FileSchema:
        return await self.repository.add(session=session, **data)

    async def delete(self, id: int, session: AsyncSession) -> int:
        await self.repository.delete(id=id, session=session)

    async def get_one(self, session: AsyncSession, **filter_by) -> FileSchema:
        return await self.repository.find_one_or_none(session=session, **filter_by)

    async def get_all(self, session: AsyncSession, **data) -> list[FileSchema]:
        return await self.repository.find_all(session=session, **data)


