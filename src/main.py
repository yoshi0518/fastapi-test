import uvicorn
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, ConfigDict, field_serializer

from config import config

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    is_offer: bool | None = None

    model_config = ConfigDict(strict=True)

    @field_serializer("is_offer")
    def serialize_is_offer(self, is_offer: bool | None):
        """nullの場合はFalseを返却"""
        return False if is_offer is None else is_offer


app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(le=10), q: str | None = Query(default=None)):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict = item_dict | {"price_with_tax": price_with_tax}
    return item_dict


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host=config.fastapi_host, port=config.fastapi_port, reload=config.debug)
