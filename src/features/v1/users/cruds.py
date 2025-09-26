from sqlalchemy.sql import selectable

from db.models.users import UsersTable
from src.common.v1.cruds import BaseCrud
from src.features.v1.users.types import ConditionUserType


class UsersCrud(BaseCrud):
    model = UsersTable
    orders = "user_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionUserType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition["user_id"] is not None:
            sql = sql.where(UsersTable.user_id == condition["user_id"])

        if condition["name"] is not None:
            sql = sql.where(UsersTable.name == condition["name"])

        return sql
