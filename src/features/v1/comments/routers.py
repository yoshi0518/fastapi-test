from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.comments.controllers import CommentsController
from src.features.v1.comments.types import (
    CreateCommentSchema,
    ReadCommentSchema,
    UpdateCommentSchema,
    example_json_schema,
)

router_v1_comments = APIRouter(default_response_class=ORJSONResponse)


@router_v1_comments.get(
    "/",
    summary="コメント一覧を取得",
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
    response_model=list[ReadCommentSchema],
    response_model_exclude_unset=True,
)
async def reads_table(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    comment_id: int = Query(None, description="コメントID  ※完全一致"),
    name: str = Query(None, description="タイトル  ※部分一致"),
    columns: str | None = Query(None, description="取得項目"),
    orders: str | None = Query(None, description="並び順"),
    limit: int = Query(10, ge=1, le=300, description="1ページあたりの取得件数"),
    page: int = Query(1, ge=1, description="取得するページ"),
):
    result = await CommentsController.reads_table(
        request,
        session,
        comment_id,
        name,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(result["headers"])
    return result["data"]


@router_v1_comments.get(
    "/{id}/",
    summary="コメントを取得",
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
    response_model=ReadCommentSchema,
    response_model_exclude_unset=True,
)
async def read_table(
    request: Request,
    session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(..., description="ID"),
    columns: str | None = Query(None, description="取得項目"),
):
    return await CommentsController.read_table(
        request,
        session,
        id,
        columns,
    )


@router_v1_comments.post(
    "/",
    summary="コメントを登録",
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
    data: CreateCommentSchema = Body(..., description="登録データ"),
):
    return await CommentsController.create(
        request,
        session,
        data.model_dump(),
    )


@router_v1_comments.put(
    "/{id}/",
    summary="コメントを更新",
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
    data: UpdateCommentSchema = Body(..., description="更新データ"),
):
    return await CommentsController.update(
        request,
        session,
        id,
        data.model_dump(exclude_unset=True),
    )


@router_v1_comments.delete(
    "/{id}/",
    summary="コメントを削除",
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
    return await CommentsController.delete(
        request,
        session,
        id,
    )


@router_v1_comments.post(
    "/update/",
    summary="コメントを一括更新",
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
    return await CommentsController.exec_update(request, session)
