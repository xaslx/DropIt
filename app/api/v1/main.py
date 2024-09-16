from fastapi import APIRouter, Request, Depends, Path, BackgroundTasks, Query
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.file import FileSchema, FileSchemaOut
from app.schemas.user import UserOut
from app.utils.templating import get_template
from fastapi.templating import Jinja2Templates
from app.services.file import FileService
from app.services.dependencies import get_file_service, get_user_service
from app.services.user import UserService
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.utils.S3 import s3_client
from app.tasks.tasks import delete_file_from_s3, send_report, delete_file_admin
from exceptions import NotAccessException, UserNotFoundException, FileNotFoundException
from config import settings



main_router: APIRouter = APIRouter(tags=['Главная страница'])


TYPE_CONTENT: list[str] = ['video', 'audio', 'image']
IP_ADMINS: list[str] = settings.ip_admins.split(',')


@main_router.get('/')
async def get_main_page(
        request: Request, 
        template: Annotated[Jinja2Templates, Depends(get_template)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        page: Annotated[int | None, Query()] = 1,
    ):
    offset = (page - 1) * 15
    ip_address: str = request.client.host
    user: UserOut = await user_service.get_one(ip_address=ip_address, session=session)
    total_pages = 0
    if user:
        user_files, total_count = await file_service.get_all(session=session, user_id=user.id, offset=offset)
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
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
    
    file: FileSchemaOut = await file_service.get_one(url=file_url, session=session)
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
        session: Annotated[AsyncSession, Depends(get_async_session)],
        bg_task: BackgroundTasks
    ):

    ip_address: str = request.client.host

    user: UserOut = await user_service.get_one(ip_address=ip_address, session=session)
    file: FileSchemaOut = await file_service.get_one(id=file_id, session=session)

    if not file:
        raise FileNotFoundException

    if ip_address in IP_ADMINS:
        await file_service.delete(id=file_id, session=session)
        await s3_client.delete_file(f'{file.url}_{file.filename}')
        bg_task.add_task(
            delete_file_admin,
            file.id
        )
        return JSONResponse(content={'message': 'file success deleted'}, status_code=200)

    if not user:
        raise UserNotFoundException
    

    if file.user_id != user.id:
        raise NotAccessException
    
    await file_service.delete(id=file_id, session=session)

    filename: str = f'{file.url}_{file.filename}'
    bg_task.add_task(
        delete_file_from_s3,
        filename
    )
    
    
@main_router.post('/report/{file_id}')
async def report_file(
        file_id: Annotated[int, Path()],
        file_service: Annotated[FileService, Depends(get_file_service)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        bg_task: BackgroundTasks
    ):

    file: FileSchemaOut = await file_service.get_one(session=session, id=file_id)

    file_url: str = f'https://8351bc0d-6a77-4774-b115-72cfb172f518.selstorage.ru/{file.url}_{file.filename}'
    bg_task.add_task(
        send_report,
        file_id=file.id,
        file_url=file_url
    )