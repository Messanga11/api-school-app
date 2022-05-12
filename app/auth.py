from hashlib import algorithms_guaranteed
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from dotenv import dotenv_values
from  fastapi import status
import jwt
from models.school_model import School
from models.user_model import *
from tortoise.queryset import QuerySet

config_credentials = dotenv_values(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password):
    return pwd_context.hash(password)

async def verify_token(token: str):
    if token.find('.') == -1:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers=["WWW-Authenticate", "Bearer"]
                )
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms=["HS256"])
        if dict(payload).get("type") == "SCHOOL":
            school = await School.filter(email=payload["email"]).first()
            return school
        else:
            user = await User.get(uuid = payload["user"]["uuid"])
            return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=["WWW-Authenticate", "Bearer"]
        )

async def verify_token_school(token: str):
    if token.find('.') == -1:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers=["WWW-Authenticate", "Bearer"]
                )
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms=["HS256"])
        user = await School.get(uuid = payload["user"]["uuid"])
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=["WWW-Authenticate", "Bearer"]
        )


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(email, password, ignore_password_check: bool = False):
    user = None
    user = await QuerySet(User).get(email=email).values()

    if user and ignore_password_check:
        return user

    if user and verify_password(password, user["password"]):
        return user
    return False

async def authenticate_school(email, password):
    school = await QuerySet(School).filter(email=email).first()

    if school and await verify_password(password, school.password):
        return school
    return False

async def token_generator(email: str, password: str, ignore_password_check: bool = False, type:str="USER"):
    
    if type == "SCHOOL":
        school = await authenticate_school(email, password)
        
        if school:
            token_data = {
                "email": school.email,
                "type": "SCHOOL"
            }
            token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
    else:
        user = await authenticate_user(email, password, ignore_password_check)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers=["WWW-Authenticate", "Bearer"]
            )

        token_data = {
            "is_admin": False,
            "user": {
                "uuid": str(user["uuid"])
            },
        }

        token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")

        return token