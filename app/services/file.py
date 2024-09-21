from app.repositories.file import FileRepository

from app.schemas.file import FileSchema, FileSchemaOut


class FileService:

    def __init__(self, repository: type[FileRepository]) -> None:
        self.repository = repository

    async def create(self, **data) -> FileSchema:
        return await self.repository.add(**data)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, **filter_by) -> FileSchemaOut:
        res = await self.repository.find_one_or_none(**filter_by)
        if not res:
            return None
        return FileSchemaOut.model_validate(res)
        
    async def get_all(self, **data) -> list[FileSchema]:
        return await self.repository.find_all(**data)


