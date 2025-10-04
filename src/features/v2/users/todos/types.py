from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

example_json_schema = {
    "todo_id": 1,
    "user_id": 1,
    "title": "text",
    "completed": 0,
}


class BaseTodoSchema(BaseModel):
    todo_id: int | None = Field(None)
    user_id: int | None = Field(None)
    title: str | None = Field(None)
    completed: int | None = Field(None)


class ReadTodoSchema(BaseTodoSchema):
    id: UUID4 | None = Field(None)
    created_at: datetime | None = Field(None)
    created_by: str | None = Field(None)
    updated_at: datetime | None = Field(None)
    updated_by: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class ConditionTodoType(BaseModel):
    user_id: int | None = None
    todo_id: int | None = None
    title: str | None = None
