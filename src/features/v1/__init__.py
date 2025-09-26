from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.features.v1.users.routers import router_v1_users

router_v1 = APIRouter(default_response_class=ORJSONResponse)

# Router設定
router_v1.include_router(router_v1_users, prefix="/users")
