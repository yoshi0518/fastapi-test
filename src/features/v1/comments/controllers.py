from pprint import pprint

import requests
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from src.features.v1.comments.cruds import CommentsCrud
from src.features.v1.comments.types import ConditionCommentType


class CommentsController:
    @classmethod
    async def reads_table(
        cls,
        request: Request,
        session: AsyncSession,
        comment_id: int | None,
        name: str | None,
        columns: str | None = None,
        orders: str | None = None,
        limit: int = 10,
        page: int = 1,
    ):
        # === 取得条件設定 Start ===
        condition = ConditionCommentType(
            comment_id=None,
            name=None,
        )

        if comment_id is not None:
            condition.comment_id = comment_id

        if name is not None:
            condition.name = name
        # === 取得条件設定 End ===

        # データ取得
        result = await CommentsCrud(session).reads(
            request,
            condition,
            columns.split(",") if columns is not None else None,
            orders.split(",") if orders is not None else None,
            limit,
            page,
        )

        # 指定した取得・並べ替え項目のチェック
        if isinstance(result, dict) and "column_check" in result:
            return {
                "headers": {},
                "data": JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": result["column_check"]},
                ),
            }

        # 存在チェック
        if result["headers"]["x-total-count"] == 0:
            return {
                "headers": {},
                "data": JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "Not Found"},
                ),
            }

        return result

    @classmethod
    async def read_table(
        cls,
        request: Request,
        session: AsyncSession,
        id: str,
        columns: str | None = None,
    ):
        # データ取得
        obj = await CommentsCrud(session).read(
            request,
            id,
            columns.split(",") if columns is not None else None,
        )

        # 存在チェック(データ)
        if obj is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Not Found"},
            )

        # 存在チェック(取得項目)
        if isinstance(obj, dict) and "column_check" in obj:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": obj["column_check"]},
            )

        return obj

    @classmethod
    async def create(
        cls,
        request: Request,
        session: AsyncSession,
        data: dict,
    ):
        # 重複チェック
        count = await CommentsCrud(session).count(request, ConditionCommentType(comment_id=data["comment_id"]))
        if count > 0:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Conflict"},
            )

        # 登録
        obj = await CommentsCrud(session).create(request, data)
        return {"id": obj.id}

    @classmethod
    async def update(
        cls,
        request: Request,
        session: AsyncSession,
        id: str,
        data: dict,
    ):
        # 存在チェック
        obj = await CommentsCrud(session).read(request, id)
        if obj is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Not Found"},
            )

        # 更新準備
        if "todo_id" in data:
            del data["todo_id"]

        await CommentsCrud(session).update(request, id, data, obj)

    @classmethod
    async def delete(
        cls,
        request: Request,
        session: AsyncSession,
        id: str,
    ):
        # 存在チェック
        obj = await CommentsCrud(session).read(request, id)
        if obj is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Not Found"},
            )

        await CommentsCrud(session).delete(request, id, obj)

    @classmethod
    async def exec_update(
        cls,
        request: Request,
        session: AsyncSession,
    ):
        # 全件削除
        await CommentsCrud(session).delete_all(request)

        # データ取得
        response = requests.get("https://jsonplaceholder.typicode.com/comments")

        if config.debug is True:
            print(response.status_code)
            pprint(response.json())

        # データ追加
        for data in response.json():
            await CommentsCrud(session).create(
                request,
                {
                    "comment_id": data["id"],
                    "post_id": data["postId"],
                    "name": data["name"],
                    "email": data["email"],
                    "body": data["body"],
                },
            )

        return {"status": "success"}
