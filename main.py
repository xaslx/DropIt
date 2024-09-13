from fastapi import FastAPI
from app.api.v1.main import main_router
from app.api.v1.upload import upload_router
from fastapi.staticfiles import StaticFiles


app: FastAPI = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(main_router)
app.include_router(upload_router)