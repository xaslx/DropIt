from fastapi import APIRouter, Request, Depends, Path, BackgroundTasks, Query, Response
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.file import FileSchemaOut
from app.schemas.user import UserOut
from app.utils.templating import get_template
from fastapi.templating import Jinja2Templates
from app.services.file import FileService
from app.services.dependencies import get_file_service, get_user_service
from app.services.user import UserService
from typing import Annotated
from app.utils.S3 import s3_client
from app.tasks.tasks import delete_file_from_s3, send_report, delete_file_admin
from exceptions import NotAccessException, UserNotFoundException, FileNotFoundException
from config import settings
from redis_init import redis




main_router: APIRouter = APIRouter(tags=['Главная страница'])


TYPE_CONTENT: list[str] = ['video', 'audio', 'image']
IP_ADMINS: list[str] = settings.ip_admins.split(',')


@main_router.get('/')
async def get_main_page(
        request: Request, 
        template: Annotated[Jinja2Templates, Depends(get_template)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        page: Annotated[int | None, Query()] = 1,
    ):


    ip_address: str = request.client.host
    offset = (page - 1) * 15
    user: UserOut | None = None
    cached_data_user: None | str = await redis.get(ip_address)

    if not cached_data_user:
        user: UserOut = await user_service.get_one(ip_address=ip_address)
        if user:
            await redis.set(ip_address, user.id, ex=86400)
    else:
        user: UserOut = UserOut(id=int(cached_data_user), ip_address=ip_address)


    total_pages = 0
    if user:
        user_files, total_count = await file_service.get_all(user_id=user.id, offset=offset)
        total_pages = (total_count + 15 - 1) // 15
        return template.TemplateResponse(
            request=request, 
            name='base.html', 
            context={'user_files': user_files, 'current_page': page, 'total_pages': total_pages})
    
    return template.TemplateResponse(request=request, name='base.html', context={'user_files': [], 'total_pages': total_pages})


   

@main_router.get('/{file_url}')
async def get_main_page(
        request: Request, 
        file_url: Annotated[str, Path()],
        template: Annotated[Jinja2Templates, Depends(get_template)],
        file_service: Annotated[FileService, Depends(get_file_service)],
    ):
    cached_data = await redis.get(name=file_url)
    if not cached_data:
        file: FileSchemaOut | None = await file_service.get_one(url=file_url)
        if file:
            file_json = file.model_dump_json()
            await redis.set(name=file_url, value=file_json, ex=3600)
    else:
        file: FileSchemaOut = FileSchemaOut.model_validate_json(cached_data)

 
    if file:
        ip_address: str = request.client.host
        file_content: str = file.content_type.split('/')[0]

        if file_content in TYPE_CONTENT:
            path: str = f'{settings.url}/{file.url}_{file.filename}'
            is_admin: bool | None = None
            if ip_address in IP_ADMINS:
                is_admin = True
            else:
                is_admin = False
            download_url: str = await s3_client.get_file(f'{file.url}_{file.filename}')

            return template.TemplateResponse(request=request, name='file.html', context={
                'file': file,
                'file_url': path,
                'download_url': download_url,
                'is_admin': is_admin
            })
        return RedirectResponse(f'{settings.url}/{file.url}_{file.filename}')
    return template.TemplateResponse(request=request, name='404.html')
        


@main_router.delete('/{file_id}')
async def delete_file(
        request: Request,
        file_id: Annotated[int, Path()],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        bg_task: BackgroundTasks
    ):

    ip_address: str = request.client.host

    user: UserOut = await user_service.get_one(ip_address=ip_address)
    file: FileSchemaOut = await file_service.get_one(id=file_id)

    if not file:
        raise FileNotFoundException

    if ip_address in IP_ADMINS:
        await file_service.delete(id=file_id)
        await s3_client.delete_file(f'{file.url}_{file.filename}')
        bg_task.add_task(
            delete_file_admin,
            file.id
        )
        await redis.delete(file.url)
        return JSONResponse(content={'message': 'file success deleted'}, status_code=200)

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
    
    
@main_router.post('/report/{file_id}')
async def report_file(
        file_id: Annotated[int, Path()],
        file_service: Annotated[FileService, Depends(get_file_service)],
        bg_task: BackgroundTasks
    ):

    file: FileSchemaOut = await file_service.get_one(id=file_id)

    file_url: str = f'{settings.url}/{file.url}_{file.filename}'
    bg_task.add_task(
        send_report,
        file_id=file.id,
        file_url=file_url
    )