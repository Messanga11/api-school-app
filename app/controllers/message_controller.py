from fastapi import APIRouter, Depends
from schema.message import MessageIn
from controllers.auth_controller import get_current_user
from tortoise.query_utils import Prefetch
from tortoise.queryset import Q

from auth import *
from models.user_model import *
from models.message_model import *


router = APIRouter(
    prefix="/administration/messages",
    tags=["message"]
)

@router.get("/conversations")
async def get_conversation(current_user=Depends(get_current_user)):
    return {
        "data": await Conversation.filter(members__uuid = current_user.uuid).prefetch_related(
            Prefetch('members', queryset=User.get(uuid=current_user.uuid))
        ).all()
    }


@router.post("")
async def create_message(message: MessageIn, current_user = Depends(get_current_user)):
    message_obj = message.dict(exclude_unset=True)

    conversation = None
    if not message_obj.get("receiver_uuid"):
        raise HTTPException(
            status_code=400,
            detail="Don't try me"
        )
    if not message_obj.get("conversation_uuid"):
        conversation = await Conversation.filter(
            Q( members__uuid=message_obj.get("receiver_uuid")) | Q( members__uuid=message_obj.get("receiver_uuid"))
        ).first()
        
        if not conversation:
            conversation = await Conversation.create()
    else:
        conversation = await Conversation.get(uuid=message_obj.get("conversation_uuid"))
    
    if not conversation:
        raise HTTPException(
            status_code=400,
            detail="No conversation found"
        )
    
    user = await User.get(uuid=message_obj.get("receiver_uuid"))
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user found"
        )
    
    await conversation.members.add(user)
    await conversation.members.add(current_user)
    
    message_obj = await Message.create(receiver=user, text=message_obj["text"], conversation_id=conversation.uuid)
    
    new_message = await message_pydantic.from_tortoise_orm(message_obj)
    return new_message

@router.get("/{conversation_uuid}")
async def get_messages(conversation_uuid: str):
    return {
        "data": await Message.filter(conversation_id=conversation_uuid)
    }

@router.get("/{id}")
async def get_messages(id: int):
    message = await Message.get(id=id)
    return message

@router.put("/{id}")
async def get_messages(id: int, message_in: message_pydanticIn):
    message_obj = message_in.dict(exclude_unset=True)
    message = await Message.get(id=id)
    if message:
        message_db = await message.update_from_dict(message_obj)
        message_db.save()
    return await message_pydanticOut.from_tortoise_orm(message_db)

@router.delete("/{id}")
async def delete_message(id: int):
    message_in = await Message.get(id=id)
    if message_in:
        await message_in.delete()
    
    return {
        "message": "Deleted"
    }