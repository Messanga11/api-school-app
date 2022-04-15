from typing import Any, List, Optional
from pydantic import BaseModel
from models.user_model import User
from models.user_model import user_pydanticOut


class MessageIn(BaseModel):
    text: str
    receiver_uuid: str
    conversation_uuid: Optional[str] = None

class MessageOut(BaseModel):
    text: str
    owners: List[user_pydanticOut]
    
class ConversationOut(BaseModel):
    uuid: str
    members: List[Any]
    last_message: str
    class Config:
        orm_mode = True