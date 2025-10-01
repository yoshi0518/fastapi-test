from fastapi import Request
from sqlalchemy.sql import selectable

from db.models.posts import PostsTable
from src.common.v1.cruds import BaseCrud
from src.features.v1.posts.types import ConditionPostType


class PostsCrud(BaseCrud):
    model = PostsTable
    orders = "post_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionPostType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.post_id is not None:
            sql = sql.where(PostsTable.post_id == condition.post_id)

        if condition.title is not None:
            sql = sql.where(PostsTable.title.contains(condition.title))

        return sql

    async def read(
        self,
        request: Request,
        id: str,
        columns: list[str] | None = None,
    ) -> PostsTable | dict | None:
        """取得"""

        return await super().read(request, id, columns)

    async def create(
        self,
        request: Request,
        data: dict,
        commit: bool = True,
    ) -> PostsTable:
        """登録"""

        return await super().create(request, data, commit)
