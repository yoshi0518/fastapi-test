import json
import math
from datetime import datetime, timedelta, timezone
from pprint import pprint
from typing import TypeVar

from fastapi import Request
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, selectable

from config import config
from db import Base
from src.utils.v1.json import type_serializer

# タイムゾーン生成
JST = timezone(timedelta(hours=+9), "JST")

# Generic用型パラメータ
T = TypeVar("T")

# モデルタイプ
ModelType = TypeVar("ModelType", bound=Base)


class BaseCrud:
    model: type[ModelType]
    session: AsyncSession
    orders: str

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def get_dblog_dict(self, request: Request):
        """RequestオブジェクトからリクエストID、実行日時、ユーザーIDを取得"""
        return {
            "request_id": getattr(request.state, "request_id", None),
            "request_date": getattr(request.state, "request_date", None),
            "request_user_id": getattr(request.state, "request_user_id", None),
        }

    def check_exists_column(self, columns: list | None) -> bool:
        """指定項目の存在チェック"""
        if columns is not None:
            for column in columns:
                if column[0] == "-":
                    if not hasattr(self.model, column[1:]):
                        return True
                else:
                    if not hasattr(self.model, column):
                        return True

        return False

    async def get_range(self, request: Request, condition: T, limit: int, page: int):
        """取得開始位置・件数を取得、ヘッダー情報準備"""
        # データ件数
        total_count = await self.count(request, condition)

        # 取得結果0件の場合
        if total_count == 0:
            return {"total_count": 0}

        # 最大ページ数
        if limit == total_count:
            max_page = 1
        else:
            max_page = math.ceil(total_count / limit)

        # 取得ページ
        if page > max_page:
            page = max_page

        # 取得開始位置
        if page == 1:
            offset = 0
        else:
            offset = limit * (page - 1)

        return {
            "total_count": total_count,
            "max_page": max_page,
            "page": page,
            "offset": offset,
        }

    def set_select_filter(self, sql: selectable.Select, condition: T) -> selectable.Select:
        """抽出条件を追加したSQLを返却"""
        return sql

    def set_delete_filter(self, sql: selectable.Select, condition: T) -> selectable.Select:
        """削除条件を追加したSQLを返却"""
        return sql

    def set_order(self, sql: selectable.Select, orders: list) -> selectable.Select:
        """並び順を追加したSQLを返却"""

        for order in orders:
            if order[0] == "-":
                if hasattr(self.model, order[1:]):
                    sql = sql.order_by((getattr(self.model, order[1:])).desc())
            else:
                if hasattr(self.model, order):
                    sql = sql.order_by(getattr(self.model, order))

        return sql

    async def count(self, request: Request, condition: T) -> int:
        """件数取得"""

        # === SELECT ===
        sql = select(func.count(self.model.id).label("count"))

        # === WHERE ===
        sql = self.set_select_filter(sql, condition)

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table_name"] = self.model.__tablename__
            log["sql_type"] = "count"
            log["sql"] = str(sql).replace("\n", "")
            log["condition"] = condition.model_dump()  # ty: ignore[unresolved-attribute]

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

        return (await self.session.execute(sql)).scalars().first()

    async def reads(
        self,
        request: Request,
        condition: T,
        columns: list[str] | None = None,
        orders: list[str] | None = None,
        limit: int = 10,
        page: int = 1,
    ) -> dict:
        """一覧取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # 指定した並べ替え項目が存在しない場合
        check_orders = self.check_exists_column(orders)
        if check_orders is True:
            return {"column_check": "Order Column Not Found"}

        # 取得件数が0件の場合
        range_info = await self.get_range(request, condition, limit, page)
        if range_info["total_count"] == 0:
            return {
                "data": [],
                "headers": {"x-total-count": 0},
            }

        # === SELECT ===
        if columns is None:
            sql = select(self.model)
        else:
            sql = select(*[getattr(self.model, column) for column in columns if hasattr(self.model, column)])

        # === WHERE ===
        sql = self.set_select_filter(sql, condition)

        # === ORDER BY ===
        if orders is not None:
            sql = self.set_order(sql, orders)
        elif self.orders is not None:
            sql = self.set_order(sql, self.orders.split(","))

        # === OFFSET ===
        if range_info["offset"] > 0:
            sql = sql.offset(range_info["offset"])

        # === LIMIT ===
        if limit is not None and limit < range_info["total_count"]:
            sql = sql.limit(limit)

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "reads"
            log["sql"] = str(sql).replace("\n", "")
            log["condition"] = condition.model_dump()  # ty: ignore[unresolved-attribute]
            log["offset"] = range_info["offset"]
            log["limit"] = limit

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

        data = (await self.session.execute(sql)).scalars().all()
        headers = {
            "x-total-count": str(range_info["total_count"]),
            "x-count": str(len(data)),
            "x-max-page": str(range_info["max_page"]),
            "x-page": str(range_info["page"]),
        }

        return {
            "data": data,
            "headers": headers,
        }

    async def read(
        self,
        request: Request,
        id: str,
        columns: list[str] | None = None,
    ) -> ModelType | dict | None:
        """取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # === SELECT ===
        if columns is None:
            sql = select(self.model).where(self.model.id == id)
        else:
            sql = select(*[getattr(self.model, column) for column in columns if hasattr(self.model, column)]).where(
                self.model.id == id
            )

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "read"
            log["sql"] = str(sql).replace("\n", "")
            log["id"] = id

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

    async def create(
        self,
        request: Request,
        data: dict,
        commit: bool = True,
    ) -> ModelType:
        """登録"""

        # 登録準備
        obj = self.model()
        for key, value in data.items():
            if hasattr(obj, key) and key not in [
                "id",
                "created_at",
                "created_by",
                "updated_at",
                "updated_by",
            ]:
                setattr(obj, key, value)
        obj.created_at = datetime.now(JST)
        obj.created_by = request.state.request_user_id if hasattr(request.state, "request_user_id") else "NonLoginFunc"
        obj.updated_at = datetime.now(JST)
        obj.updated_by = request.state.request_user_id if hasattr(request.state, "request_user_id") else "NonLoginFunc"

        # 登録
        self.session.add(obj)
        if commit:
            await self.session.commit()
            await self.session.refresh(obj)

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "create"
            log["commit"] = commit
            log["data"] = data
            log["id"] = obj.id

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

        return obj

    async def update(
        self,
        request: Request,
        id: str,
        data: dict,
        obj: ModelType,
        commit: bool = True,
    ):
        """更新"""

        # 更新準備
        for key, value in data.items():
            if hasattr(obj, key) and key not in [
                "id",
                "created_at",
                "created_by",
            ]:
                setattr(obj, key, value)
        obj.updated_at = datetime.now(JST)
        obj.updated_by = request.state.request_user_id if hasattr(request.state, "request_user_id") else "NonLoginFunc"

        # 更新
        self.session.add(obj)
        if commit:
            await self.session.commit()
            await self.session.refresh(obj)

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "update"
            log["commit"] = commit
            log["data"] = data
            log["id"] = id

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

    async def delete(
        self,
        request: Request,
        id: str,
        obj: ModelType,
        commit: bool = True,
    ):
        """削除"""

        # 削除
        await self.session.delete(obj)
        if commit:
            await self.session.commit()

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "delete"
            log["commit"] = commit
            log["id"] = id

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

    async def delete_filter(
        self,
        request: Request,
        condition: T,
        commit: bool = True,
    ):
        """条件削除"""

        # === DELETE ===
        sql = delete(self.model)

        # === WHERE ===
        sql = self.set_delete_filter(sql, condition)

        # 条件削除
        await self.session.execute(sql)
        if commit:
            await self.session.commit()

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "delete_filter"
            log["commit"] = commit
            log["sql"] = str(sql).replace("\n", "")
            log["condition"] = condition.model_dump()  # ty: ignore[unresolved-attribute]

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

    async def delete_all(
        self,
        request: Request,
        commit: bool = True,
    ):
        """全件削除"""

        # === DELETE ===
        sql = delete(self.model)

        # 全件削除
        await self.session.execute(sql)
        if commit:
            await self.session.commit()

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "delete_all"
            log["commit"] = commit
            log["sql"] = str(sql).replace("\n", "")

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

    async def get_select_sql(
        self,
        request: Request,
        condition: T,
        columns: list[str] | None = None,
        orders: list[str] | None = None,
        limit: int = 10,
        page: int = 1,
    ) -> selectable.Select | dict:
        """SELECT SQL取得"""

        # 指定した取得項目が存在しない場合
        check_columns = self.check_exists_column(columns)
        if check_columns is True:
            return {"column_check": "Select Column Not Found"}

        # 指定した並べ替え項目が存在しない場合
        check_orders = self.check_exists_column(orders)
        if check_orders is True:
            return {"column_check": "Order Column Not Found"}

        # 取得件数が0件の場合
        range_info = await self.get_range(request, condition, limit, page)
        if range_info["total_count"] == 0:
            return {
                "data": [],
                "headers": {"x-total-count": 0},
            }

        # === SELECT ===
        if columns is None:
            sql = select(self.model)
        else:
            sql = select(*[getattr(self.model, column) for column in columns if hasattr(self.model, column)])

        # === WHERE ===
        sql = self.set_select_filter(sql, condition)

        # === ORDER BY ===
        if orders is not None:
            sql = self.set_order(sql, orders)
        elif self.orders is not None:
            sql = self.set_order(sql, self.orders.split(","))

        # === OFFSET ===
        if range_info["offset"] > 0:
            sql = sql.offset(range_info["offset"])

        # === LIMIT ===
        if limit is not None and limit < range_info["total_count"]:
            sql = sql.limit(limit)

        # === DB操作ログ出力 Start ===
        if config.debug:
            log: dict = self.get_dblog_dict(request)
            log["table"] = self.model.__tablename__
            log["type"] = "get_select_sql"
            log["sql"] = str(sql).replace("\n", "")
            log["condition"] = condition.model_dump()  # ty: ignore[unresolved-attribute]
            log["offset"] = range_info["offset"]
            log["limit"] = limit

            print("=== ↓↓↓ Db Access Log ↓↓↓ ===")
            pprint(json.dumps(log, default=type_serializer, ensure_ascii=False))
            print("=== ↑↑↑ Db Access Log ↑↑↑ ===")
        # === DB操作ログ出力 End ===

        return sql
