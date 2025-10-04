import hashlib
from datetime import UTC, datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from config import config

# Asia/Tokyoタイムゾーンを定義
JST = timezone(timedelta(hours=+9), "JST")

# ログイン認証スキーマ
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v2/login/")


# パスワードをハッシュ化
def get_digest(password: str) -> str:
    return hashlib.sha256(bytes(config.oauth_secret_key + password, "utf-8")).hexdigest()


# トークン作成
def create_token(user_id: str, expire_minutes: int, token_type: str) -> str:
    created_utc_dt = datetime.now(UTC)
    created_jst_dt = datetime.now(JST)
    return jwt.encode(
        {
            "sub": user_id,
            "id": user_id,
            "token_type": token_type,
            "exp": created_utc_dt + timedelta(minutes=expire_minutes),
            "created_dt": created_jst_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "expired_dt": (created_jst_dt + timedelta(minutes=expire_minutes)).strftime("%Y-%m-%d %H:%M:%S"),
        },
        config.oauth_secret_key,
        algorithm=config.oauth_algorithm,
    )
