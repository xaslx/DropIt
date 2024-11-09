from fastapi import APIRouter, Request, Depends, Path, BackgroundTasks, Query, Response
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.file import FileSchemaOut
from app.schemas.user import UserIn, UserOut
from app.utils.templating import get_template
from fastapi.templating import Jinja2Templates
from app.services.file import FileService
from app.services.dependencies import get_file_service, get_user_service, get_async_redis
from app.services.user import UserService
from typing import Annotated
from app.utils.S3 import s3_client
from app.tasks.tasks import delete_file_from_s3
from exceptions import NotAccessException, UserNotFoundException, FileNotFoundException
from config import settings
from redis.asyncio import Redis
from uuid import uuid4, UUID
from datetime import datetime, timedelta, timezone



main_router: APIRouter = APIRouter(tags=['Главная страница'])


TYPE_CONTENT: list[str] = ['video', 'audio', 'image']


@main_router.get('/')
async def get_main_page(
        request: Request, 
        response: Response,
        template: Annotated[Jinja2Templates, Depends(get_template)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        page: Annotated[int | None, Query()] = 1,
    ):


    cookie_uuid: str = request.cookies.get('cookie_uuid')
    total_pages: int = 0
    if cookie_uuid:
        user: UserOut | None = await user_service.get_user(cookie_uuid=cookie_uuid)
        
        if user:
            offset: int = (page - 1) * 15
            user_files, total_count = await file_service.get_all(user_id=user.id, offset=offset)
            total_pages: int = (total_count + 15 - 1) // 15

            return template.TemplateResponse(
                request=request, 
                name='base.html', 
                context={'user_files': user_files, 'current_page': page, 'total_pages': total_pages})
        return template.TemplateResponse(
                    request=request, 
                    name='base.html', 
                    context={'user_files': [], 'total_pages': total_pages}, 
                )
    else:
        new_uuid: UUID = uuid4()
        response = template.TemplateResponse(
                    request=request, 
                    name='base.html', 
                    context={'user_files': [], 'total_pages': total_pages}, 
                )
        current_date: datetime = datetime.now(timezone.utc) + timedelta(days=2000)
        response.set_cookie(key='cookie_uuid', value=str(new_uuid), httponly=True, expires=current_date)
        await user_service.create(cookie_uuid=str(new_uuid))
        return response



   

@main_router.get('/{file_url}')
async def get_main_page(
        request: Request, 
        file_url: Annotated[str, Path()],
        template: Annotated[Jinja2Templates, Depends(get_template)],
        file_service: Annotated[FileService, Depends(get_file_service)],
    ):

    file = await file_service.get_one_with_cache(file_url)
    if file:
        file_content: str = file.content_type.split('/')[0]

        if file_content in TYPE_CONTENT:
            path: str = f'{settings.url}/{file.url}_{file.filename}'
            download_url: str = await s3_client.get_file(f'{file.url}_{file.filename}')

            return template.TemplateResponse(request=request, name='file.html', context={
                'file': file,
                'file_url': path,
                'download_url': download_url,
            })
        return RedirectResponse(f'{settings.url}/{file.url}_{file.filename}')
    return template.TemplateResponse(request=request, name='404.html')
        


@main_router.delete('/{file_id}')
async def delete_file(
        request: Request,
        file_id: Annotated[int, Path()],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        redis: Annotated[Redis, Depends(get_async_redis)],
        bg_task: BackgroundTasks
    ):

    cookie_uuid: str = request.cookies.get('cookie_uuid')

    user: UserOut = await user_service.get_user(cookie_uuid=cookie_uuid)
    file: FileSchemaOut = await file_service.get_one(id=file_id)

    if not file:
        raise FileNotFoundException

    if not user:
        raise UserNotFoundException
    
    if file.user_id != user.id:
        raise NotAccessException
    
    await file_service.delete(id=file_id)
    await redis.delete(file.url)
    filename: str = f'{file.url}_{file.filename}'
    bg_task.add_task(
        delete_file_from_s3,
        filename
    )
