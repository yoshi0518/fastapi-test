from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import SMALLINT, TEXT, VARCHAR

from db.models import Base, BaseTable

Base = Base


class CommentssTable(BaseTable):
    __tablename__ = "t_comments"
    __table_args__ = (
        UniqueConstraint("comment_id"),
        {"comment": "コメント"},
    )

    comment_id = Column(SMALLINT, nullable=False)
    post_id = Column(SMALLINT)
    name = Column(VARCHAR(200))
    email = Column(VARCHAR(200))
    body = Column(TEXT)
