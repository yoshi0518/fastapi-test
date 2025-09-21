# https://docs.pydantic.dev/latest/concepts/pydantic_settings/
import os
from pprint import pprint

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Common
    debug: bool = True

    # FastAPI
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_title: str = "FastAPI(Local)"
    fastapi_version: str = "1.0.0"

    # Cors
    cors_allow_origins: str = "http://localhost:3000"


config = Config()

if __name__ == "__main__":
    for c in config:
        print(c)
        pprint(type(c[1]))
