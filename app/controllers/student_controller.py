import math
from fastapi import APIRouter, Depends
from utils import get_image_full_url
from core.settings import AppConfig
from schema.student_custom_schema import AcceptInvitationIn
from schema.student_custom_schema import InvitationOutSchema
from models.friend_match_model import FriendMatch, friend_match_pydanticOut
from schema.student_custom_schema import InvitationSchema
from controllers.auth_controller import get_current_user
from tortoise.queryset import Q

from auth import *
from models.user_model import *


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_user(user: user_pydanticIn):
    user_obj = user.dict(exclude_unset=True)
    
    print(user_obj)
    hashed_password = get_hashed_password(user_obj["password"])
    
    user_obj["password"] = hashed_password
    
    
    user_obj = await User.create(**user_obj)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return new_user

@router.get("/friends")
async def get_friends(current_user=Depends(get_current_user), page:int=1, per_page:int=10, keyword:str="",):
    
    query_set = FriendMatch.filter(Q(request_user_id=current_user.uuid)| Q(main_user_uuid=current_user.uuid)).filter(accepted=True)
    
    if len(keyword) > 0:
        query_set = query_set.filter(Q(request_user__first_name__icontains=f"{keyword}")| Q(request_user__last_name__icontains=f"{keyword}"))
    
    total = await query_set.count()
    
    query_set = query_set\
        .offset(per_page*(page-1))\
        .limit(per_page)
    invitations = await query_set.all()
    
    data = []
    for invitation in invitations:
        user = await User.get(uuid=invitation.main_user_uuid).first()
        user.image_url = get_image_full_url(user.image_url)
        if user.uuid == current_user.uuid:
            user = await User.get(uuid=invitation.request_user_id).first()
        data.append({**dict(invitation), "request_user": user})
    
    return {
        'total': total,
        "data": data,
        "current_page": page,
        "per_page": per_page,
        "pages":  math.ceil(total/per_page) if per_page != 0 else 0
    }

@router.post("/send-invitation")
async def send_invitation(payload: InvitationSchema, current_user = Depends(get_current_user)):
    friend_match = payload.dict(exclude_unset=True)
    
    user_as_sender = await FriendMatch.filter(request_user_id=current_user.uuid)
    user_as_sender = await FriendMatch.filter(request_user_id=friend_match["second_user_uuid"])
    
    user_as_recever = await FriendMatch.filter(main_user_uuid=current_user.uuid)
    user_as_recever = await FriendMatch.filter(main_user_uuid=friend_match["second_user_uuid"])
    
    if user_as_recever or user_as_sender:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="An invitation request has already been sent."
        )
    
    friend_match = await FriendMatch.create(request_user_id=friend_match["second_user_uuid"], main_user_uuid=current_user.uuid, accepted=False)

    # friend_match = await friend_match_pydanticOut.from_tortoise_orm(friend_match)
    return friend_match

@router.get("/invitations/get")
async def get_invitations(current_user = Depends(get_current_user), page:int=1, per_page:int=10, keyword:str=""):
    query_set = FriendMatch.filter(request_user_id=current_user.uuid).filter(accepted=False)
    
    if len(keyword) > 0:
        query_set = query_set.filter(Q(request_user__first_name__icontains=f"{keyword}")| Q(request_user__last_name__icontains=f"{keyword}"))
    
    total = await query_set.count()
    
    query_set = query_set\
        .offset(per_page*(page-1))\
        .limit(per_page)

    invitations = await query_set.all()
    
    data = []
    for invitation in invitations:
        user = await invitation.request_user.first()
        data.append({**dict(invitation), "request_user": user})
    
    return {
        "total": total,
        "per_page": per_page,
        "current_page": page,
        "data": data,
        "pages":  math.ceil(total/per_page) if per_page != 0 else 0
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
async def get_users(current_user = Depends(get_current_user), page:int=1, per_page:int=10, keyword:str=""):
    
    query_set = User.exclude(uuid = current_user.uuid)
    
    if len(keyword) > 0:
        query_set = query_set.filter(Q(first_name__icontains=f"{keyword}")| Q(last_name__icontains=f"{keyword}"))
    
    total = await query_set.count()
    
    query_set = query_set\
        .offset(per_page*(page-1))\
        .limit(per_page)

    users = await query_set.all()
    
    users_to_send = []
    for user in users:
        user_as_sender = await FriendMatch.filter(request_user_id=current_user.uuid, main_user_uuid=user.uuid).filter(accepted=True).all()
        user_as_recever = await FriendMatch.filter(main_user_uuid=current_user.uuid, request_user_id=user.uuid).filter(accepted=True).all()
        user.image_url = get_image_full_url(user.image_url)
        user = {
            **dict(user),
            "is_friend": True if ((len(user_as_recever) > 0) or (len(user_as_sender) > 0)) else False,
        }
        users_to_send.append(user)
    return {
        "total": total,
        "per_page": per_page,
        "current_page": page,
        "data": users_to_send,
        "pages":  math.ceil(total/per_page) if per_page != 0 else 0
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

@router.delete("/{uuid}")
async def delete_user(uuid: str):
    user_in = await User.get(uuid=uuid)
    if user_in:
        await user_in.delete()
    
    return {
        "message": "Deleted"
    }