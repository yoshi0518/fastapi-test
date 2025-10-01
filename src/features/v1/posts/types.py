from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

example_json_schema = {
    "post_id": 1,
    "user_id": 1,
    "title": "text",
    "body": "text",
}


class BasePostSchema(BaseModel):
    post_id: int | None = Field(None)
    user_id: int | None = Field(None)
    title: str | None = Field(None)
    body: str | None = Field(None)


class ReadPostSchema(BasePostSchema):
    id: UUID4 | None = Field(None)
    created_at: datetime | None = Field(None)
    created_by: str | None = Field(None)
    updated_at: datetime | None = Field(None)
    updated_by: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class CreatePostSchema(BasePostSchema):
    post_id: int = Field(...)

    model_config = ConfigDict(from_attributes=True)


class UpdatePostSchema(BasePostSchema):
    model_config = ConfigDict(from_attributes=True)


class ConditionPostType(BaseModel):
    post_id: int | None = None
    title: str | None = None
