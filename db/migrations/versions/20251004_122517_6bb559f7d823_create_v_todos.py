"""create v_todos

Revision ID: 6bb559f7d823
Revises: 9d1b9f166528
Create Date: 2025-10-04 12:25:17.833997+09:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6bb559f7d823"
down_revision: str | Sequence[str] | None = "9d1b9f166528"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
CREATE VIEW v_todos AS
SELECT
  t_todos.todo_id,
  t_todos.user_id,
  t_users.name,
  t_users.username,
  t_todos.title,
  t_todos.completed,
  CASE
    t_todos.completed
    WHEN 0 THEN '未完了'
    WHEN 1 THEN '完了'
  END AS "completed_name",
  t_todos.id,
  t_todos.created_at,
  t_todos.created_by,
  t_todos.updated_at,
  t_todos.updated_by
FROM
  t_todos
  INNER JOIN t_users ON t_users.user_id = t_todos.user_id
;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_todos;")
