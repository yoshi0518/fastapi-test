import uvicorn
from fastapi import FastAPI

from config import config

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None) -> dict[str, str | int | None]:
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host=config.fastapi_host, port=config.fastapi_port, reload=config.debug)
