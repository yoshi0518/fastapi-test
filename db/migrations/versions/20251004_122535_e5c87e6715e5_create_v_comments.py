"""create v_comments

Revision ID: e5c87e6715e5
Revises: efe5d38a115b
Create Date: 2025-10-04 12:25:35.905472+09:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5c87e6715e5"
down_revision: str | Sequence[str] | None = "efe5d38a115b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
CREATE VIEW v_comments AS
SELECT
  t_comments.comment_id,
  t_comments.post_id,
  t_posts.user_id,
  t_users.name,
  t_users.username,
  t_posts.title AS "post_title",
  t_posts.body AS "post_body",
  t_comments.name AS "comment_name",
  t_comments.email AS "comment_email",
  t_comments.body AS "comment_body",
  t_comments.id,
  t_comments.created_at,
  t_comments.created_by,
  t_comments.updated_at,
  t_comments.updated_by
FROM
  t_comments
  INNER JOIN t_posts ON t_posts.post_id = t_comments.post_id
  INNER JOIN t_users ON t_users.user_id = t_posts.user_id
;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW v_comments;")
