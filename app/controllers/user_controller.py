from fastapi import APIRouter, Depends
from controllers.auth_controller import get_current_user

from auth import *
from models.user_model import *


router = APIRouter(
    prefix="/administration/users",
    tags=["user"]
)


@router.post("/")
async def create_user(user: user_pydanticIn, logged_user_data: user_pydanticOut=Depends(get_current_user)):
    user_obj = user.dict(exclude_unset=True)
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