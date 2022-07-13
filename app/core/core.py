import pathlib
import os
import io
import uuid
from functools import lru_cache
from fastapi import(
    FastAPI,
    Header,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile
    )

from pydantic import BaseSettings
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    app_auth_token: str
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
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


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
        raise HTTPException(detail="Invalid endpoint", status_code=401)
    label, token = authorization.split()
    if token != settings.app_auth_token:
        raise HTTPException(detail="Invalid token credentials", status_code=401)