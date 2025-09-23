from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import SMALLINT, VARCHAR

from db.models import Base, BaseTable

Base = Base


class TodosTable(BaseTable):
    __tablename__ = "t_todos"
    __table_args__ = (
        UniqueConstraint("todo_id"),
        {"comment": "ToDo"},
    )

    todo_id = Column(SMALLINT, nullable=False)
    user_id = Column(SMALLINT)
    title = Column(VARCHAR(200))
    completed = Column(SMALLINT)
