from fastapi import APIRouter, File, UploadFile, Depends, Request
from typing import Annotated
from app.schemas.user import UserIn, UserOut
from app.services.user import UserService
from app.services.file import FileService
import secrets
from app.services.dependencies import get_user_service, get_file_service
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from app.schemas.file import FileSchema
from datetime import datetime
from app.utils.S3 import s3_client
from exceptions import FileTooLargeException


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
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
    if file.size > 210000000:
        raise FileTooLargeException
    ip_address: str = request.client.host
    user: UserOut = await user_service.get_one(ip_address=ip_address, session=session)

    if not user:
        new_user: UserIn = UserIn(ip_address=ip_address)
        user: UserOut = await user_service.create(session=session, **new_user.model_dump())

    unique_filename: str = secrets.token_urlsafe(4)
    current_datetime: datetime = datetime.now()
    new_file: FileSchema = FileSchema(filename=file.filename, url=unique_filename, upload_date=current_datetime, user_id=user.id, content_type=file.content_type)
    
    await file_service.create(session=session, **new_file.model_dump())
    await s3_client.upload_file(file.file, f'{unique_filename}_{file.filename}')


  