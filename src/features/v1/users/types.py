from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

example_json_schema = {
    "user_id": 1,
    "name": "text",
    "username": "text",
    "email": "text",
    "address_street": "text",
    "address_suite": "text",
    "address_city": "text",
    "address_zipcode": "text",
    "geo_lat": 123.45,
    "geo_lng": 123.45,
    "phone": "text",
    "website": "text",
    "company_name": "text",
    "company_catch_phrase": "text",
    "company_bs": "text",
}


class BaseUserSchema(BaseModel):
    user_id: int | None = Field(None)
    name: str | None = Field(None)
    username: str | None = Field(None)
    email: str | None = Field(None)
    address_street: str | None = Field(None)
    address_suite: str | None = Field(None)
    address_city: str | None = Field(None)
    address_zipcode: str | None = Field(None)
    geo_lat: float | None = Field(None)
    geo_lng: float | None = Field(None)
    phone: str | None = Field(None)
    website: str | None = Field(None)
    company_name: str | None = Field(None)
    company_catch_phrase: str | None = Field(None)
    company_bs: str | None = Field(None)


class ReadUserSchema(BaseUserSchema):
    id: UUID4 | None = Field(None)
    created_at: datetime | None = Field(None)
    created_by: str | None = Field(None)
    updated_at: datetime | None = Field(None)
    updated_by: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(BaseUserSchema):
    user_id: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseUserSchema):
    model_config = ConfigDict(from_attributes=True)


class ConditionUserType(BaseModel):
    user_id: int | None = None
    name: str | None = None
