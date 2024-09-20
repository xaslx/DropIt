from fastapi import APIRouter, File, UploadFile, Depends, Request, BackgroundTasks
from typing import Annotated
from app.schemas.user import UserIn, UserOut
from app.services.user import UserService
from app.services.file import FileService
import secrets
from app.services.dependencies import get_user_service, get_file_service, get_blacklist_service
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from app.schemas.file import FileSchema, FileSchemaOut
from datetime import datetime
from app.utils.S3 import s3_client
from exceptions import FileTooLargeException, NotAccessException
from app.services.blacklist import BlackListService
from app.schemas.blacklist import BlackList
from app.tasks.tasks import add_new_file
from config import settings



upload_router: APIRouter = APIRouter(
    prefix='/upload',
    tags=['Загрузка файла']
)



@upload_router.post('')
async def upload_file(
        request: Request, 
        file: Annotated[UploadFile, File()], 
        user_service: Annotated[UserService, Depends(get_user_service)], 
        file_service: Annotated[FileService, Depends(get_file_service)],
        blacklist_service: Annotated[BlackListService, Depends(get_blacklist_service)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        bg_task: BackgroundTasks
    ):

    if file.size > 210000000:
        raise FileTooLargeException
    
    ip_address: str = request.client.host

    user_in_blacklist: BlackList = await blacklist_service.get_one(ip_address=ip_address, session=session)
    if not user_in_blacklist:
        user: UserOut = await user_service.get_one(ip_address=ip_address, session=session)

        if not user:
            new_user: UserIn = UserIn(ip_address=ip_address)
            user: UserOut = await user_service.create(session=session, **new_user.model_dump())

        unique_filename: str = secrets.token_urlsafe(4)
        current_datetime: datetime = datetime.now()
        new_file: FileSchemaOut = FileSchema(filename=file.filename, url=unique_filename, upload_date=current_datetime, user_id=user.id, content_type=file.content_type)
        
        output: FileSchemaOut = await file_service.create(session=session, **new_file.model_dump())
        await s3_client.upload_file(file.file, f'{unique_filename}_{file.filename}')
        bg_task.add_task(
            add_new_file,
            output.id,
            f'{settings.url}/{unique_filename}_{file.filename}'
        )
    else:
        raise NotAccessException


    