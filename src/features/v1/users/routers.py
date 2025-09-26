from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.users.controllers import UsersController
from src.features.v1.users.types import ReadUserSchema, example_json_schema

router_v1_users = APIRouter(default_response_class=ORJSONResponse)


@router_v1_users.get(
    "/",
    summary="ユーザー一覧を取得",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            **example_json_schema,
                            **{
                                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                "created_at": "2026-01-01T00:00:00",
                                "created_by": "text",
                                "updated_at": "2026-01-01T00:00:00",
                                "updated_by": "text",
                            },
                        }
                    ],
                },
            },
        },
        401: {
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"},
                },
            },
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Not Found"}},
            },
        },
    },
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
    response = await UsersController.reads_table(
        request,
        session,
        user_id,
        name,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(response["headers"])
    return response["data"]
