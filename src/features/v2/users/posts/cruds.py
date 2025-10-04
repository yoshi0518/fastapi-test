import json
from pprint import pprint

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.sql import selectable

from config import config
from db.models.posts import PostsTable
from src.common.v2.cruds import BaseCrud
from src.features.v2.users.posts.types import ConditionPostType
from src.utils.v2.json import type_serializer


class PostsCrud(BaseCrud):
    model = PostsTable
    orders = "post_id"

    def set_select_filter(self, sql: selectable.Select, condition: ConditionPostType) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""

        if condition.user_id is not None:
            sql = sql.where(PostsTable.user_id == condition.user_id)

        if condition.post_id is not None:
            sql = sql.where(PostsTable.post_id == condition.post_id)

        if condition.title is not None:
            sql = sql.where(PostsTable.title.contains(condition.title))

        return sql

    async def read(
        self,
        request: Request,
        user_id: int,
        post_id: int,
        columns: list[str] | None = None,
    ) -> PostsTable | dict | None:
        """取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # === SELECT ===
        if columns is None:
            sql = select(PostsTable).where(PostsTable.user_id == user_id, PostsTable.post_id == post_id)
        else:
            sql = select(*[getattr(PostsTable, column) for column in columns if hasattr(PostsTable, column)]).where(
                PostsTable.user_id == user_id, PostsTable.post_id == post_id
            )

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = PostsTable.__tablename__
            log["type"] = "read"
            log["sql"] = str(sql).replace("\n", "")
            log["user_id"] = user_id
            log["post_id"] = post_id

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
