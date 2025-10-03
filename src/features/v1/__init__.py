from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.features.v1.comments.routers import router_v1_comments
from src.features.v1.login.routers import router_v1_login
from src.features.v1.posts.routers import router_v1_posts
from src.features.v1.todos.routers import router_v1_todos
from src.features.v1.users.routers import router_v1_users
from src.utils.v1.login import oauth2_scheme

router_v1 = APIRouter(default_response_class=ORJSONResponse)

# Router設定
router_v1.include_router(router_v1_login, prefix="/login")
router_v1.include_router(router_v1_users, prefix="/users", dependencies=[Depends(oauth2_scheme)])
router_v1.include_router(router_v1_todos, prefix="/todos", dependencies=[Depends(oauth2_scheme)])
router_v1.include_router(router_v1_posts, prefix="/posts", dependencies=[Depends(oauth2_scheme)])
router_v1.include_router(router_v1_comments, prefix="/comments", dependencies=[Depends(oauth2_scheme)])
