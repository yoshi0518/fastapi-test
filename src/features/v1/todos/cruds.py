from fastapi import Request
from sqlalchemy.sql import selectable

from db.models.todos import TodosTable
from src.common.v1.cruds import BaseCrud
from src.features.v1.todos.types import ConditionTodoType


class TodosCrud(BaseCrud):
    model = TodosTable
    orders = "todo_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionTodoType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.todo_id is not None:
            sql = sql.where(TodosTable.todo_id == condition.todo_id)

        if condition.title is not None:
            sql = sql.where(TodosTable.title.contains(condition.title))

        return sql

    async def read(
        self,
        request: Request,
        id: str,
        columns: list[str] | None = None,
    ) -> TodosTable | dict | None:
        """取得"""

        return await super().read(request, id, columns)

    async def create(
        self,
        request: Request,
        data: dict,
        commit: bool = True,
    ) -> TodosTable:
        """登録"""

        return await super().create(request, data, commit)
