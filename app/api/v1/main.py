from fastapi import APIRouter, Request, Depends
from app.utils.templating import get_template
from fastapi.templating import Jinja2Templates



main_router: APIRouter = APIRouter()


@main_router.get('/')
async def get_main_page(request: Request, template: Jinja2Templates = Depends(get_template)):
    return template.TemplateResponse(request=request, name='base.html', context={'msg': 'hello'})