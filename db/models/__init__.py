import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Asia/Tokyoタイムゾーンを定義
JST = timezone(timedelta(hours=9))


def now_jst():
    """現在時刻をAsia/Tokyoタイムゾーンで返す"""
    return datetime.now(JST)


class BaseTable(Base):
    """BaseTable"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=now_jst,
        server_default=text("NOW() AT TIME ZONE 'Asia/Tokyo'"),
    )
    created_by = Column(VARCHAR(100), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=now_jst,
        onupdate=now_jst,
        server_default=text("NOW() AT TIME ZONE 'Asia/Tokyo'"),
    )
    updated_by = Column(VARCHAR(100), nullable=False)
