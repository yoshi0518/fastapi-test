from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.users.controllers import UsersController
from src.features.v1.users.types import ReadUserSchema

router_v1_users = APIRouter(default_response_class=ORJSONResponse)


@router_v1_users.get(
    "/",
    summary="ユーザー一覧を取得",
    responses={},
    response_model=list[ReadUserSchema],
    response_model_exclude_unset=True,
)
async def reads_table(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    user_id: int = Query(None, description="ユーザーID  ※部分一致"),
    name: str = Query(None, description="ユーザー名  ※部分一致"),
    columns: str | None = Query(None, description="取得項目"),
    orders: str | None = Query(None, description="並び順"),
    limit: int = Query(10, ge=1, le=300, description="1ページあたりの取得件数"),
    page: int = Query(1, ge=1, description="取得するページ"),
):
    data = await UsersController.reads_table(
        request,
        session,
        user_id,
        name,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(data["headers"])
    return data["contents"]
