from fastapi import APIRouter, Request, Depends
from app.schemas.user import UserOut
from app.utils.templating import get_template
from fastapi.templating import Jinja2Templates
from app.services.file import FileService
from app.services.dependencies import get_file_service, get_user_service
from app.services.user import UserService
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated



main_router: APIRouter = APIRouter(tags=['Главная страница'])


@main_router.get('/')
async def get_main_page(
        request: Request, 
        template: Annotated[Jinja2Templates, Depends(get_template)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
    ):

    ip_address: str = request.client.host
    user: UserOut = await user_service.get_one(ip_address=ip_address, session=session)

    if user:
        list_files: list[FileService] = await file_service.get_all(session=session, user_id=user.id)
        return template.TemplateResponse(request=request, name='base.html', context={'user_files': list_files})
    
    return template.TemplateResponse(request=request, name='base.html', context={'user_files': []})