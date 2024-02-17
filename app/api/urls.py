from config.app_run import app
from fastapi import APIRouter
from app.api.v1 import views as api
urls = APIRouter()


# Meta URLs
@urls.get("/")
def root():
    return {'message': 'Arkon Test'}


urls.include_router(api.router, prefix="/api/v1")


app.include_router(urls)
