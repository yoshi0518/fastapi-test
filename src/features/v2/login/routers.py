from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from src.features.v2.login.controllers import LoginController
from src.features.v2.login.types import ReadLoginSchema, example_json_schema

router_v2_login = APIRouter(default_response_class=ORJSONResponse)


@router_v2_login.post(
    "/",
    summary="ログイン認証(アクセス・リフレッシュトークン発行)",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": example_json_schema,
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {"detail": "Not Found"},
                },
            },
        },
    },
    response_model=ReadLoginSchema,
    response_model_exclude_unset=True,
)
async def reads_table(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    form: OAuth2PasswordRequestForm = Depends(),
):
    return await LoginController.create(
        request,
        session,
        form.username,
        form.password,
    )
