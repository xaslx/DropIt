from fastapi import APIRouter, File, UploadFile, Depends, Request, BackgroundTasks, Response
from typing import Annotated
from datetime import datetime, timezone
from uuid import uuid4, UUID
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.schemas.user import UserIn, UserOut
from app.services.user import UserService
from app.services.file import FileService
import secrets
from app.services.dependencies import get_user_service, get_file_service, get_blacklist_service
from app.schemas.file import FileSchema, FileSchemaOut
from datetime import datetime, timedelta, timezone
from app.utils.S3 import s3_client
from app.utils.templating import get_template
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
        response: Response,
        file: Annotated[UploadFile, File()], 
        user_service: Annotated[UserService, Depends(get_user_service)], 
        file_service: Annotated[FileService, Depends(get_file_service)],
        blacklist_service: Annotated[BlackListService, Depends(get_blacklist_service)],
        template: Annotated[Jinja2Templates, Depends(get_template)],
        bg_task: BackgroundTasks
    ):

    if file.size > 110000000:
        raise FileTooLargeException
    
    ip_address: str = request.client.host
    user_in_blacklist: BlackList = await blacklist_service.get_one(ip_address=ip_address)
    

    if not user_in_blacklist:
        cookie: str = request.cookies.get('cookie_uuid')
        user: UserOut = await user_service.get_user(cookie_uuid=cookie)
        if user:
            unique_filename: str = secrets.token_urlsafe(4)
            current_datetime: datetime = datetime.now()
            new_file: FileSchemaOut = FileSchema(
                filename=file.filename, 
                url=unique_filename, 
                upload_date=current_datetime, 
                user_id=user.id, 
                content_type=file.content_type
            )
            file_content = await file.read()
            output: FileSchemaOut = await file_service.create(**new_file.model_dump())
            await s3_client.upload_file(file_content, f'{unique_filename}_{file.filename}')
            bg_task.add_task(
                add_new_file,
                output.id,
                f'{settings.url}/{unique_filename}_{file.filename}'
            )
            return JSONResponse(content={'success': 'New File Add'}, status_code=200)
        else:
            new_uuid: UUID = uuid4()
            current_date: datetime = datetime.now(timezone.utc) + timedelta(days=2000)
            response = JSONResponse(content={'message': 'Перезагрузите страницу'}, status_code=400)
            response.set_cookie(key='cookie_uuid', value=str(new_uuid), httponly=True, expires=current_date)
            await user_service.create(cookie_uuid=str(new_uuid))
            return response
    else:
        raise NotAccessException
