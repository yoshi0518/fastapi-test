# https://docs.pydantic.dev/latest/concepts/pydantic_settings/
import os
from pprint import pprint

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env読み込み
load_dotenv()


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

    # OAuth
    oauth_user: str = "xxxxxxxxxx"
    oauth_pass: str = "xxxxxxxxxx"
    oauth_secret_key: str = "xxxxxxxxxx"
    oauth_algorithm: str = "HS256"
    oauth_expire_minutes_access_token: int = 60
    oauth_expire_minutes_refresh_token: int = 10080

    # Neon
    neon_host: str = "xxxxxxxxxx"
    neon_db: str = "xxxxxxxxxx"
    neon_user: str = "xxxxxxxxxx"
    neon_password: str = "xxxxxxxxxx"


config = Config()

if __name__ == "__main__":
    for c in config:
        print(c)
        pprint(type(c[1]))
