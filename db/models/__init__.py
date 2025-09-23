import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Asia/Tokyoタイムゾーンを定義
JST = timezone(timedelta(hours=9))


def now_jst():
    """Asia/Tokyoタイムゾーンで現在日時を取得"""
    return datetime.now(JST)


class BaseTable(Base):
    """BaseTable"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=now_jst,
    )
    created_by = Column(VARCHAR(100), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=now_jst,
        onupdate=now_jst,
    )
    updated_by = Column(VARCHAR(100), nullable=False)
