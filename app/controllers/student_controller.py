from fastapi import APIRouter, Depends
from schema.student_custom_schema import AcceptInvitationIn
from schema.student_custom_schema import InvitationOutSchema
from models.friend_match_model import FriendMatch, friend_match_pydanticOut
from schema.student_custom_schema import InvitationSchema
from controllers.auth_controller import get_current_user

from auth import *
from models.user_model import *


router = APIRouter(
    prefix="/administration/users",
    tags=["users"]
)


@router.post("")
async def create_user(user: user_pydanticIn):
    user_obj = user.dict(exclude_unset=True)
    
    hashed_password = get_hashed_password(user_obj["password"])
    
    user_obj["password"] = hashed_password
    
    user_obj = await User.create(**user_obj)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return new_user

@router.get("/friends")
async def get_friends(current_user=Depends(get_current_user)):
    invitations = await FriendMatch.filter(request_user_id=current_user.uuid).filter(accepted=True).all()
    
    data = []
    for invitation in invitations:
        user = await invitation.request_user.first()
        data.append({**dict(invitation), "request_user": user})
    
    return {
        "data": data
    }

@router.post("/send-invitation")
async def send_invitation(payload: InvitationSchema, current_user = Depends(get_current_user)):
    friend_match = payload.dict(exclude_unset=True)
    
    user_as_sender = await FriendMatch.filter(request_user_id=current_user.uuid)
    
    user_as_recever = await FriendMatch.filter(main_user_uuid=current_user.uuid)
    
    if user_as_recever or user_as_sender:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not able to perform this action."
        )
    
    friend_match = await FriendMatch.create(request_user=current_user, main_user_uuid=friend_match["second_user_uuid"], accepted=False)

    # friend_match = await friend_match_pydanticOut.from_tortoise_orm(friend_match)
    return friend_match

@router.get("/invitations/get")
async def get_invitations(current_user = Depends(get_current_user)):
    
    invitations = await FriendMatch.filter(request_user_id=current_user.uuid).filter(accepted=False).all()
    
    data = []
    for invitation in invitations:
        user = await invitation.request_user.first()
        data.append({**dict(invitation), "request_user": user})
    
    return {
        "data": data
    }

@router.post("/accept-invitation")
async def get_invitations(obj_in:AcceptInvitationIn, current_user = Depends(get_current_user)):
    
    obj_in = obj_in.dict(exclude_unset=True)
    
    friend_match = await FriendMatch.filter(uuid=obj_in["invitation_uuid"]).filter(request_user_id=current_user.uuid).first()
    
    if not friend_match:
        raise HTTPException(
            status_code=400,
            detail="Your are not able to perform this action"
        )
    
    await friend_match.update_from_dict({"accepted": True})
    await friend_match.save()
    await friend_match.refresh_from_db()

    return {
        "message": friend_match
    }

@router.delete("/remove-friend")
async def remove_friend(obj_in:AcceptInvitationIn, current_user=Depends(get_current_user)):
    
    obj_in = obj_in.dict(exclude_unset=True)
    
    friend_match = await FriendMatch.get(uuid=obj_in["invitation_uuid"])
    
    if not friend_match:
        raise HTTPException(
            status_code=400,
            detail="Your are not able to perform this action"
        )
    
    if (dict(friend_match)["request_user_id"] == current_user.uuid) or (dict(friend_match)["main_user_uuid"] == current_user.uuid) :
    
        await friend_match.delete()

        return {
            "message": "ok"
        }
        
    raise HTTPException(
        status_code=400,
        detail="Your are not able to perform this action"
    )
    
    
@router.get("")
async def get_users(current_user = Depends(get_current_user)):
    users = await User.exclude(uuid = current_user.uuid).all()
    users_to_send = []
    for user in users:
        user_as_sender = await FriendMatch.filter(request_user_id=current_user.uuid)
    
        user_as_recever = await FriendMatch.filter(main_user_uuid=current_user.uuid)
        user = {
            **dict(user),
            "is_friend": True if (user_as_recever or user_as_sender) else False,
            "img_url": "https://images.unsplash.com/photo-1614023342667-6f060e9d1e04?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8YWZyaWNhbiUyMG1hbnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=400&q=60"
        }
        users_to_send.append(user)
    return {
        "data": users_to_send
    }

@router.get("/{id}")
async def get_user(id: int):
    user = await User.get(id=id)
    return user

@router.put("")
async def update_users(user_in: user_pydanticIn, current_user=Depends(get_current_user)):
    user = await User.get(uuid=current_user.uuid)
    user_obj = user_in.dict(exclude_unset=True)
    if user:
        user_db = await user.update_from_dict(user_obj)
        await user_db.save()
        await user.refresh_from_db()
        return await user_pydanticOut.from_tortoise_orm(user_db)
    else:
        raise HTTPException(
            status_code=404,
            detail="User not exists"
        )

@router.delete("/{id}")
async def delete_user(id: int):
    user_in = await User.get(id=id)
    if user_in:
        await user_in.delete()
    
    return {
        "message": "Deleted"
    }