import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseTable(Base):
    """BaseTable"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    created_by = Column(VARCHAR(100), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    updated_by = Column(VARCHAR(100), nullable=False)
