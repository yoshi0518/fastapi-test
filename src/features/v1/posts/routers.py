from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v1.posts.controllers import PostsController
from src.features.v1.posts.types import CreatePostSchema, ReadPostSchema, UpdatePostSchema, example_json_schema

router_v1_posts = APIRouter(default_response_class=ORJSONResponse)


@router_v1_posts.get(
    "/",
    summary="投稿一覧を取得",
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
    response_model=list[ReadPostSchema],
    response_model_exclude_unset=True,
)
async def reads_table(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    post_id: int = Query(None, description="投稿ID  ※完全一致"),
    title: str = Query(None, description="タイトル  ※部分一致"),
    columns: str | None = Query(None, description="取得項目"),
    orders: str | None = Query(None, description="並び順"),
    limit: int = Query(10, ge=1, le=300, description="1ページあたりの取得件数"),
    page: int = Query(1, ge=1, description="取得するページ"),
):
    result = await PostsController.reads_table(
        request,
        session,
        post_id,
        title,
        columns,
        orders,
        limit,
        page,
    )

    response.headers.update(result["headers"])
    return result["data"]


@router_v1_posts.get(
    "/{id}/",
    summary="投稿を取得",
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
    response_model=ReadPostSchema,
    response_model_exclude_unset=True,
)
async def read_table(
    request: Request,
    session: AsyncSession = Depends(get_db),
    id: UUID4 = Path(..., description="ID"),
    columns: str | None = Query(None, description="取得項目"),
):
    return await PostsController.read_table(
        request,
        session,
        id,
        columns,
    )


@router_v1_posts.post(
    "/",
    summary="投稿を登録",
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
    data: CreatePostSchema = Body(..., description="登録データ"),
):
    return await PostsController.create(
        request,
        session,
        data.model_dump(),
    )


@router_v1_posts.put(
    "/{id}/",
    summary="投稿を更新",
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
    data: UpdatePostSchema = Body(..., description="更新データ"),
):
    return await PostsController.update(
        request,
        session,
        id,
        data.model_dump(exclude_unset=True),
    )


@router_v1_posts.delete(
    "/{id}/",
    summary="投稿を削除",
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
    return await PostsController.delete(
        request,
        session,
        id,
    )
