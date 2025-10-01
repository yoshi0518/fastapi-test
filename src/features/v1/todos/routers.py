from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.todos.controllers import TodosController
from src.features.v1.todos.types import CreateTodoSchema, ReadTodoSchema, UpdateTodoSchema, example_json_schema

router_v1_todos = APIRouter(default_response_class=ORJSONResponse)


@router_v1_todos.get(
    "/",
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
        todo_id,
        title,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(result["headers"])
    return result["data"]


@router_v1_todos.get(
    "/{id}/",
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
    id: UUID4 = Path(..., description="ID"),
    columns: str | None = Query(None, description="取得項目"),
):
    return await TodosController.read_table(
        request,
        session,
        id,
        columns,
    )


@router_v1_todos.post(
    "/",
    summary="TODOを登録",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {"id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"},
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
        409: {
            "content": {
                "application/json": {
                    "example": {"detail": "Conflict"},
                },
            },
        },
    },
)
async def create(
    request: Request,
    session: AsyncSession = Depends(get_db),
    data: CreateTodoSchema = Body(..., description="登録データ"),
):
    return await TodosController.create(
        request,
        session,
        data.model_dump(),
    )


@router_v1_todos.put(
    "/{id}/",
    summary="TODOを更新",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
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
)
async def update(
    request: Request,
    session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(..., description="ID"),
    data: UpdateTodoSchema = Body(..., description="更新データ"),
):
    return await TodosController.update(
        request,
        session,
        id,
        data.model_dump(exclude_unset=True),
    )


@router_v1_todos.delete(
    "/{id}/",
    summary="TODOを削除",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
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
)
async def delete(
    request: Request,
    session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(..., description="ID"),
):
    return await TodosController.delete(
        request,
        session,
        id,
    )


@router_v1_todos.post(
    "/update/",
    summary="TODOを一括更新",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {"status": "success"},
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
    },
)
async def exec_update(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    return await TodosController.exec_update(request, session)
