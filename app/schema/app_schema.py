from typing import Any, List
from pydantic import BaseModel


class DataList(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int
    data: List[Any] = []

    class Config:
        orm_mode = True