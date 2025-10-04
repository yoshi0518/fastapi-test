import json
from pprint import pprint

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.sql import selectable

from config import config
from db.models.todos import TodosTable
from src.common.v2.cruds import BaseCrud
from src.features.v2.users.todos.types import ConditionTodoType
from src.utils.v2.json import type_serializer


class TodosCrud(BaseCrud):
    model = TodosTable
    orders = "todo_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionTodoType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.user_id is not None:
            sql = sql.where(TodosTable.user_id == condition.user_id)

        if condition.todo_id is not None:
            sql = sql.where(TodosTable.todo_id == condition.todo_id)

        if condition.title is not None:
            sql = sql.where(TodosTable.title.contains(condition.title))

        return sql

    async def read(
        self,
        request: Request,
        user_id: int,
        todo_id: int,
        columns: list[str] | None = None,
    ) -> TodosTable | dict | None:
        """取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # === SELECT ===
        if columns is None:
            sql = select(TodosTable).where(TodosTable.user_id == user_id, TodosTable.todo_id == todo_id)
        else:
            sql = select(*[getattr(TodosTable, column) for column in columns if hasattr(TodosTable, column)]).where(
                TodosTable.user_id == user_id, TodosTable.todo_id == todo_id
            )

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = TodosTable.__tablename__
            log["type"] = "read"
            log["sql"] = str(sql).replace("\n", "")
            log["user_id"] = user_id
            log["todo_id"] = todo_id

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

        data = (await self.session.execute(sql)).first()

        if data is None:
            return None
        elif columns is None:
            return data[0]
        else:
            return data
