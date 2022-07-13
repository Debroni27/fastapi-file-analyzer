import pathlib
import logging
import uvicorn
from functools import lru_cache

from fastapi.middleware.wsgi import WSGIMiddleware

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends,
    )

from pydantic import BaseSettings


from app.controllers.DashboardRouter import dashboard

# App settings
app = FastAPI(title="Analyzer API")
app.include_router(dashboard, prefix='/api/dashboard')

# Logger init
logging.basicConfig(filename="log.txt", level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')


class Settings(BaseSettings):
    app_auth_token: str = None
    debug: bool = False
    echo_active: bool = False
    app_auth_token_prod: str = None
    skip_auth: bool = False

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
DEBUG = settings.debug

BASE_DIR = pathlib.Path(__file__).parent


def verify_auth(authorization=Header(None), settings: Settings = Depends(get_settings)):
    """
    Authorization: Bearer <token>
    {"authorization": "Bearer <token>"}
    :param authorization:
    :param settings:
    :return:
    """
    if settings.debug and settings.skip_auth:
        return
    if authorization is None:
        logging.debug("Invalid endpoint")
        raise HTTPException(detail="Invalid endpoint", status_code=401)
    label, token = authorization.split()
    if token != settings.app_auth_token:
        logging.debug("Invalid token credentials")
        raise HTTPException(detail="Invalid token credentials", status_code=401)


@app.get('/')
def index():
    return "Hello"

if __name__ == "__main__":
    uvicorn.run("core:app", host="127.0.0.1", port=8080, workers=2, reload=True)