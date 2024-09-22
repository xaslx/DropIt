from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.v1.main import main_router
from app.api.v1.upload import upload_router
from fastapi.staticfiles import StaticFiles
from app.bot.run import on_startup
from logger import logger
from contextlib import asynccontextmanager
from config import settings
from app.bot.run import handle_web_hook
from app.utils.templating import get_template


template: Jinja2Templates = get_template()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    logger.info("Fastapi приложение и Бот запущены")
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
    )

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(main_router)
app.include_router(upload_router)
app.add_route(f"/{settings.bot_token_tg}", handle_web_hook, methods=["POST"])


@app.exception_handler(404)
async def not_found_exception_handler(
    request: Request, 
    exc: HTTPException):

    return RedirectResponse('/')