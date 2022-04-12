from pydantic import BaseModel
from models.user_model import user_pydanticOut 

class InvitationSchema(BaseModel):
    second_user_uuid: str
    
class InvitationOutSchema(BaseModel):
    regisiter_user: user_pydanticOut
    accepted: bool

class AcceptInvitationIn(BaseModel):
    invitation_uuid: str