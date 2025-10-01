from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.users.controllers import UsersController
from src.features.v1.users.types import CreateUserSchema, ReadUserSchema, UpdateUserSchema, example_json_schema

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
    user_id: int = Query(None, description="ユーザーID  ※完全一致"),
    name: str = Query(None, description="ユーザー名  ※部分一致"),
    columns: str | None = Query(None, description="取得項目"),
    orders: str | None = Query(None, description="並び順"),
    limit: int = Query(10, ge=1, le=300, description="1ページあたりの取得件数"),
    page: int = Query(1, ge=1, description="取得するページ"),
):
    result = await UsersController.reads_table(
        request,
        session,
        user_id,
        name,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(result["headers"])
    return result["data"]


@router_v1_users.get(
    "/{id}/",
    summary="ユーザーを取得",
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
    response_model=ReadUserSchema,
    response_model_exclude_unset=True,
)
async def read_table(
    request: Request,
    session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(..., description="ID"),
    columns: str | None = Query(None, description="取得項目"),
):
    return await UsersController.read_table(
        request,
        session,
        id,
        columns,
    )


@router_v1_users.post(
    "/",
    summary="ユーザーを登録",
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
    data: CreateUserSchema = Body(..., description="登録データ"),
):
    return await UsersController.create(
        request,
        session,
        data.model_dump(),
    )


@router_v1_users.put(
    "/{id}/",
    summary="ユーザーを更新",
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
    data: UpdateUserSchema = Body(..., description="更新データ"),
):
    return await UsersController.update(
        request,
        session,
        id,
        data.model_dump(exclude_unset=True),
    )


@router_v1_users.delete(
    "/{id}/",
    summary="ユーザーを削除",
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
    return await UsersController.delete(
        request,
        session,
        id,
    )


@router_v1_users.post(
    "/update/",
    summary="ユーザーを一括更新",
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
    return await UsersController.exec_update(request, session)
