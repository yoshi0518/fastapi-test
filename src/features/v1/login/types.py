from pydantic import BaseModel, ConfigDict, Field

example_json_schema = {
    "access_token": "text",
    "refresh_token": "text",
    "token_type": "text",
    "user_id": "text",
}


class ReadLoginSchema(BaseModel):
    access_token: str | None = Field(None)
    refresh_token: str | None = Field(None)
    token_type: str | None = Field(None)
    user_id: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)
