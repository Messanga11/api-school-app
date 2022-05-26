from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Request, status
from utils import get_image_full_url
from core.settings import AppConfig
from models.user_model import *
from auth import *
from models.guardian_model import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#Signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    return user

async def is_superAdmin(token:str):
    user = await get_current_user(token)
    if not user.role == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Action not allowed",
            headers=["WWW-Authenticate", "Bearer"]
        )
    else:
        return user

@router.post("/token")
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/me")
async def user_infos(user: Union[User, School] = Depends(get_current_user)):
    if isinstance(user, User):
        user.image_url = get_image_full_url(user.image_url)
    return user

@post_save(User)
async def create_guardian(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:

    if created:
        guardian_obj = await Guardian.create(
            phone_number = instance.guardian_phone_number
        )
        await guardian_pydantic.from_tortoise_orm(guardian_obj)
        # Send message

#Register a user
@router.post("/registration")
async def user_registration(user: user_pydanticIn):
    user_infos = user.dict(exclude_unset=True)
    user_infos["password"] = get_hashed_password(user_infos["password"])
    user_obj = await User.create(**user_infos)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status": "ok",
        "data": f"Hello {new_user.user_name}, thanks for your registration, check the link in email inbox we just sent."
    }

@router.post("/login/school")
async def user_registration(login_form: login_schema):
    login_infos = login_form.dict(exclude_unset=True)
    token = await token_generator(login_infos["email"], login_infos["password"], False, type="SCHOOL")
    return {
        "message": "Connected successfully",
        "token": token,
        "type": "SCHOOL"
    }

@router.post("/login")
async def user_registration(login_form: login_schema):
    login_infos = login_form.dict(exclude_unset=True)
    token = await token_generator(login_infos["email"], login_infos["password"])
    return {
        "message": "Connected successfully",
        "token": token,
        "type": "STUDENT"
    }
    
@router.post("/login/{guardian_phone_number}")
async def user_registration(guardian_phone_number: int):
    login_infos = await User.filter(guardian_phone_number=guardian_phone_number).first()
    if not login_infos:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid phone number",
        headers=["WWW-Authenticate", "Bearer"]
        )
    token = await token_generator(login_infos.email, login_infos.password, False)
    return {
        "message": "Connected successfully",
        "token": token,
    }

templates = Jinja2Templates(directory="templates")

@router.get("/verification", response_class = HTMLResponse)
async def email_verification(request:Request, token:str):
    user = await verify_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html",{"request": request, "username": user.user_name})
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=["WWW-Authenticate", "Bearer"]
        )