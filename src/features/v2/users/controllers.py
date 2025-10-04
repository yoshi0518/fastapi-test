from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.v2.users.cruds import UsersCrud
from src.features.v2.users.types import ConditionUserType


class UsersController:
    @classmethod
    async def reads_table(
        cls,
        request: Request,
        session: AsyncSession,
        user_id: int | None,
        name: str | None,
        columns: str | None = None,
        orders: str | None = None,
        limit: int = 10,
        page: int = 1,
    ):
        # === 取得条件設定 Start ===
        condition = ConditionUserType(
            user_id=None,
            name=None,
        )

        if user_id is not None:
            condition.user_id = user_id

        if name is not None:
            condition.name = name
        # === 取得条件設定 End ===

        # データ取得
        result = await UsersCrud(session).reads(
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
        user_id: int,
        columns: str | None = None,
    ):
        # データ取得
        obj = await UsersCrud(session).read(
            request,
            user_id,
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
