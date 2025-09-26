from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.v1.users.cruds import UsersCrud
from src.features.v1.users.types import ConditionUserType


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
        condition: ConditionUserType = {
            "user_id": None,
            "name": None,
        }

        if user_id is not None:
            condition["user_id"] = user_id

        if name is not None:
            condition["name"] = name
        # === 取得条件設定 End ===

        # データ取得
        response = await UsersCrud(session).reads(
            request,
            condition,
            columns.split(",") if columns is not None else None,
            orders.split(",") if orders is not None else None,
            limit,
            page,
        )

        # 指定した取得・並べ替え項目のチェック
        if isinstance(response, dict) and "column_check" in response:
            return {
                "headers": {},
                "contents": JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": response["column_check"]},
                ),
            }

        # 存在チェック
        if response["headers"]["x-total-count"] == 0:
            return {
                "headers": {},
                "contents": JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "Not Found"},
                ),
            }

        return response
