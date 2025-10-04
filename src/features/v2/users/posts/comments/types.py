from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

example_json_schema = {
    "comment_id": 1,
    "post_id": 1,
    "name": "text",
    "email": "text",
    "body": "text",
}


class BaseCommentSchema(BaseModel):
    comment_id: int | None = Field(None)
    post_id: int | None = Field(None)
    name: str | None = Field(None)
    email: str | None = Field(None)
    body: str | None = Field(None)


class ReadCommentSchema(BaseCommentSchema):
    id: UUID4 | None = Field(None)
    created_at: datetime | None = Field(None)
    created_by: str | None = Field(None)
    updated_at: datetime | None = Field(None)
    updated_by: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class ConditionCommentType(BaseModel):
    user_id: int | None = None
    post_id: int | None = None
    comment_id: int | None = None
    name: str | None = None
