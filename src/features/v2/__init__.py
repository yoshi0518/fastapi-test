from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.features.v2.login.routers import router_v2_login
from src.features.v2.users.routers import router_v2_users
from src.utils.v2.login import oauth2_scheme

router_v2 = APIRouter(default_response_class=ORJSONResponse)

# Router設定
router_v2.include_router(router_v2_login, prefix="/login")
router_v2.include_router(router_v2_users, prefix="/users", dependencies=[Depends(oauth2_scheme)])
