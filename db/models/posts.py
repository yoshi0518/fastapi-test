from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import SMALLINT, TEXT, VARCHAR

from db.models import Base, BaseTable

Base = Base


class PostsTable(BaseTable):
    __tablename__ = "t_posts"
    __table_args__ = (
        UniqueConstraint("post_id"),
        {"comment": "投稿"},
    )

    post_id = Column(SMALLINT, nullable=False)
    user_id = Column(SMALLINT)
    title = Column(VARCHAR(200))
    body = Column(TEXT)
