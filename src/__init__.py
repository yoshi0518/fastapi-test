import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from config import config
from db import get_db
from src.features.v1 import router_v1

app = FastAPI(
    title=config.fastapi_title,
    version=config.fastapi_version,
    default_response_class=ORJSONResponse,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_allow_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def read_root(request: Request, session: AsyncSession = Depends(get_db)):
    return {"hello": "world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# Router設定
app.include_router(router_v1, prefix="/v1")


if __name__ == "__main__":
    uvicorn.run("src:app", host=config.fastapi_host, port=config.fastapi_port, reload=config.debug)
