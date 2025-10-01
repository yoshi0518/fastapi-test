from fastapi import Request
from sqlalchemy.sql import selectable

from db.models.comments import CommentsTable
from src.common.v1.cruds import BaseCrud
from src.features.v1.comments.types import ConditionCommentType


class CommentsCrud(BaseCrud):
    model = CommentsTable
    orders = "comment_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionCommentType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.comment_id is not None:
            sql = sql.where(CommentsTable.comment_id == condition.comment_id)

        if condition.name is not None:
            sql = sql.where(CommentsTable.name.contains(condition.name))

        return sql

    async def read(
        self,
        request: Request,
        id: str,
        columns: list[str] | None = None,
    ) -> CommentsTable | dict | None:
        """取得"""

        return await super().read(request, id, columns)

    async def create(
        self,
        request: Request,
        data: dict,
        commit: bool = True,
    ) -> CommentsTable:
        """登録"""

        return await super().create(request, data, commit)
