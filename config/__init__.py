# https://docs.pydantic.dev/latest/concepts/pydantic_settings/
import os
from pprint import pprint

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str
    debug: bool

    fastapi_host: str
    fastapi_port: int
    fastapi_title: str
    fastapi_version: str

    class Config:
        env_file = os.path.dirname(os.path.abspath(__file__)) + "/.env"


config = Config()

if __name__ == "__main__":
    for c in config:
        pprint(c)
        pprint(type(c[1]))
