import hashlib
from datetime import timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from config import config

# Asia/Tokyoタイムゾーンを定義
JST = timezone(timedelta(hours=9))

# ログイン認証スキーマ
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login/")


# パスワードをハッシュ化
def get_digest(password: str) -> str:
    return hashlib.sha256(bytes(config.oauth_secret + password, "utf-8")).hexdigest()


# トークン作成


# トークン確認
