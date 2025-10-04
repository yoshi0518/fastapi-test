import json
from pprint import pprint

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.sql import selectable

from config import config
from db.models.users import UsersTable
from src.common.v2.cruds import BaseCrud
from src.features.v2.users.types import ConditionUserType
from src.utils.v2.json import type_serializer


class UsersCrud(BaseCrud):
    model = UsersTable
    orders = "user_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionUserType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.user_id is not None:
            sql = sql.where(UsersTable.user_id == condition.user_id)

        if condition.name is not None:
            sql = sql.where(UsersTable.name.contains(condition.name))

        return sql

    async def read(
        self,
        request: Request,
        user_id: int,
        columns: list[str] | None = None,
    ) -> UsersTable | dict | None:
        """取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # === SELECT ===
        if columns is None:
            sql = select(UsersTable).where(UsersTable.user_id == user_id)
        else:
            sql = select(*[getattr(UsersTable, column) for column in columns if hasattr(UsersTable, column)]).where(
                UsersTable.user_id == user_id
            )

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = UsersTable.__tablename__
            log["type"] = "read"
            log["sql"] = str(sql).replace("\n", "")
            log["user_id"] = user_id

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
