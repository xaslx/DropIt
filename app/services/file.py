from app.repositories.file import FileRepository
from redis.asyncio import Redis
from app.schemas.file import FileSchema, FileSchemaOut
from logger import logger
import asyncio
from app.tasks.tasks import new_error



class FileService:

    def __init__(self, repository: type[FileRepository], redis: Redis | None) -> None:
        self.repository = repository
        self.redis = redis

    async def create(self, **data) -> FileSchema:
        return await self.repository.add(**data)

    async def delete(self, id: int) -> int:
        await self.repository.delete(id=id)

    async def get_one(self, **filter_by) -> FileSchemaOut:
        res = await self.repository.find_one_or_none(**filter_by)
        if not res:
            return None
        return FileSchemaOut.model_validate(res)

    async def get_one_with_cache(self, file_url: str) -> FileSchemaOut:
        if self.redis:
            try:
                cached_data: str = await self.redis.get(file_url)
                if cached_data:
                    return FileSchemaOut.model_validate_json(cached_data)
            except Exception as e:
                logger.error('Не удалось получить кэш')
                asyncio.create_task(new_error(text='Не удалось получить кэш'))

        file: FileSchemaOut | None = await self.repository.find_one_or_none(url=file_url)
        if file:
            file = FileSchemaOut.model_validate(file)
            if self.redis:
                try:
                    file_json = file.model_dump_json()
                    await self.redis.set(file_url, file_json, ex=3600)
                except Exception as e:
                    logger.error('Не удалось записать файл в кэш', e)
                    asyncio.create_task(new_error(text=f'Не удалось записать файл в кэш" {e}'))

            return FileSchemaOut.model_validate(file)
        return None
        
    async def get_all(self, **data) -> list[FileSchema]:
        return await self.repository.find_all(**data)


