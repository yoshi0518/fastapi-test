from fastapi import APIRouter, Depends, Path, Query, Request, Response
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v2.users.todos.controllers import TodosController
from src.features.v2.users.todos.types import ReadTodoSchema, example_json_schema

router_v2_todos = APIRouter(default_response_class=ORJSONResponse)


@router_v2_todos.get(
    "/{user_id}/todos/",
    summary="TODO一覧を取得",
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
    response_model=list[ReadTodoSchema],
    response_model_exclude_unset=True,
)
async def reads_table(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    user_id: int = Path(..., description="ユーザーID  ※完全一致"),
    todo_id: int = Query(None, description="TODO ID  ※完全一致"),
    title: str = Query(None, description="タイトル  ※部分一致"),
    columns: str | None = Query(None, description="取得項目"),
    orders: str | None = Query(None, description="並び順"),
    limit: int = Query(10, ge=1, le=300, description="1ページあたりの取得件数"),
    page: int = Query(1, ge=1, description="取得するページ"),
):
    result = await TodosController.reads_table(
        request,
        session,
        user_id,
        todo_id,
        title,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(result["headers"])
    return result["data"]


@router_v2_todos.get(
    "/{user_id}/todos/{todo_id}/",
    summary="TODOを取得",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        **example_json_schema,
                        **{
                            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "created_at": "2026-01-01T00:00:00",
                            "created_by": "text",
                            "updated_at": "2026-01-01T00:00:00",
                            "updated_by": "text",
                        },
                    },
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
    response_model=ReadTodoSchema,
    response_model_exclude_unset=True,
)
async def read_table(
    request: Request,
    session: AsyncSession = Depends(get_db),
    user_id: int = Path(..., description="ユーザーID"),
    todo_id: int = Path(..., description="TODO ID"),
    columns: str | None = Query(None, description="取得項目"),
):
    return await TodosController.read_table(
        request,
        session,
        user_id,
        todo_id,
        columns,
    )
