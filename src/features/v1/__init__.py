from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.features.v1.comments.routers import router_v1_comments
from src.features.v1.posts.routers import router_v1_posts
from src.features.v1.todos.routers import router_v1_todos
from src.features.v1.users.routers import router_v1_users

router_v1 = APIRouter(default_response_class=ORJSONResponse)

# Router設定
router_v1.include_router(router_v1_users, prefix="/users")
router_v1.include_router(router_v1_todos, prefix="/todos")
router_v1.include_router(router_v1_posts, prefix="/posts")
router_v1.include_router(router_v1_comments, prefix="/comments")
