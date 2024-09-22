from fastapi import FastAPI
from app.api.v1.main import main_router
from app.api.v1.upload import upload_router
from fastapi.staticfiles import StaticFiles
from app.bot.run import on_startup
from logger import logger
from contextlib import asynccontextmanager
from config import settings
from app.bot.run import handle_web_hook


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    logger.info("Fastapi приложение и Бот запущены")
    yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(main_router)
app.include_router(upload_router)
app.add_route(f"/{settings.bot_token_tg}", handle_web_hook, methods=["POST"])