from typing_extensions import TypedDict


class DblogDictType(TypedDict):
    request_id: str | None
    request_date: str | None
    request_user_id: str | None


class RangeType(TypedDict):
    total_count: int
    max_page: int
    page: int
    offset: int
