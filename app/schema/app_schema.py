from typing import Any, List
from pydantic import BaseModel, validator
from schema.message import ConversationOut

from models.user_model import user_pydanticOut


class DataList(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int
    data: List = []

    class Config:
        orm_mode = True

class DatalistResponseMembers(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int
    data: List[ConversationOut]

    @validator('data', pre=True)
    def _iter_to_list(cls, v):
        return list(v)
    
    class Config:
        orm_mode = True