from fastapi import Request
from sqlalchemy.sql import selectable

from db.models.users import UsersTable
from src.common.v1.cruds import BaseCrud
from src.features.v1.users.types import ConditionUserType


class UsersCrud(BaseCrud):
    model = UsersTable
    orders = "user_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionUserType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if "user_id" in condition and condition["user_id"] is not None:
            sql = sql.where(UsersTable.user_id == condition["user_id"])

        if "name" in condition and condition["name"] is not None:
            sql = sql.where(UsersTable.name == condition["name"])

        return sql

    async def read(
        self,
        request: Request,
        id: str,
        columns: list[str] | None = None,
    ) -> UsersTable | dict | None:
        """取得"""

        return await super().read(request, id, columns)

    async def create(
        self,
        request: Request,
        data: dict,
        commit: bool = True,
    ) -> UsersTable:
        """登録"""

        return await super().create(request, data, commit)
