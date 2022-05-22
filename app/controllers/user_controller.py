from email import message
import uuid
from fastapi import APIRouter, Depends
from schema.UserSchema import UserIn
from controllers.auth_controller import get_current_user

from auth import *
from models.user_model import *


router = APIRouter(
    prefix="/administration/users",
    tags=["user"]
)


@router.post("")
async def create_user(user: UserIn):
    user_obj = user.dict(exclude_unset=True)
    email_already_exist = await User.get_or_none(email=user_obj["email"])
    if email_already_exist:
        raise HTTPException(
            status_code=401,
            detail="A user with this email already exists"
        )
    user_name_already_exist = await User.get_or_none(user_name=user_obj["user_name"])
    if user_name_already_exist:
        raise HTTPException(
            status_code=401,
            detail="A user with this user name already exists"
        )
    phone_number_already_exist = await User.get_or_none(phone_number=user_obj["phone_number"])
    if phone_number_already_exist:
        raise HTTPException(
            status_code=401,
            detail="A user with this phone number already exists"
        )
    # guardian_phone_number_already_exist = await User.filter(guardian_phone_number=user_obj["guardian_phone_number"]).first()
    # if guardian_phone_number_already_exist:
    #     raise HTTPException(
    #         status_code=401,
    #         detail="A user with this guardian phone number already exists"
    #     )
    user_obj["password"] = get_hashed_password(user_obj["password"])
    user_obj = await User.create(**user_obj)
    new_user = await user_pydanticOut.from_tortoise_orm(user_obj)
    return new_user

@router.get("/")
async def get_users():
    users = await User.all()
    return users

@router.get("/{id}")
async def get_users(id: int):
    user = await User.get(id=id)
    return user

@router.put("")
async def get_users(user_in: user_pydanticIn):
    user_obj = user_in.dict(exclude_unset=True)
    user = await User.get(uuid=user_in["uuid"])
    if user:
        user_db = await user.update_from_dict(user_obj)
        user_db.save()
    return await user_pydanticOut.from_tortoise_orm(user_db)

@router.delete("/{id}")
async def delete_user(id: int):
    user_in = await User.get(id=id)
    if user_in:
        await user_in.delete()
    
    return {
        "message": "Deleted"
    }