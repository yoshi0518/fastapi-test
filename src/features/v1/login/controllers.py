from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from src.utils.v1.login import create_token


class LoginController:
    @classmethod
    async def create(
        cls,
        request: Request,
        session: AsyncSession,
        user_id: str,
        password: str,
    ):
        if user_id != config.oauth_user or password != config.oauth_pass:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="パスワードに誤りがあります。")

        return {
            "access_token": create_token(
                user_id,
                config.oauth_expire_minutes_access_token,
                "access_token",
            ),
            "refresh_token": create_token(
                user_id,
                config.oauth_expire_minutes_refresh_token,
                "access_token",
            ),
            "token_type": "bearer",
            "user_id": user_id,
        }
