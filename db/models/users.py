from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import REAL, SMALLINT, VARCHAR

from db.models import Base, BaseTable

Base = Base


class UsersTable(BaseTable):
    __tablename__ = "t_users"
    __table_args__ = (
        UniqueConstraint("user_id"),
        {"comment": "ユーザー"},
    )

    user_id = Column(SMALLINT, nullable=False)
    name = Column(VARCHAR(200))
    username = Column(VARCHAR(200))
    email = Column(VARCHAR(200))
    address_street = Column(VARCHAR(200))
    address_suite = Column(VARCHAR(200))
    address_city = Column(VARCHAR(200))
    address_zipcode = Column(VARCHAR(200))
    geo_lat = Column(REAL)
    geo_lng = Column(REAL)
    phone = Column(VARCHAR(200))
    website = Column(VARCHAR(200))
    company_name = Column(VARCHAR(200))
    company_catch_phrase = Column(VARCHAR(200))
    company_bs = Column(VARCHAR(200))
