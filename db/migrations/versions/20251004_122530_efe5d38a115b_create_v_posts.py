"""create v_posts

Revision ID: efe5d38a115b
Revises: 6bb559f7d823
Create Date: 2025-10-04 12:25:30.024035+09:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "efe5d38a115b"
down_revision: str | Sequence[str] | None = "6bb559f7d823"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
CREATE VIEW v_posts AS
SELECT
  t_posts.post_id,
  t_posts.user_id,
  t_users.name,
  t_users.username,
  t_posts.title,
  t_posts.body,
  t_posts.id,
  t_posts.created_at,
  t_posts.created_by,
  t_posts.updated_at,
  t_posts.updated_by
FROM
  t_posts
  INNER JOIN t_users ON t_users.user_id = t_posts.user_id
;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_posts;")
