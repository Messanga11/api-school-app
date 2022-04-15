
from dataclasses import dataclass
from enum import unique
from tortoise import Model, fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from core.settings import AppConfig


class User(Model):
    uuid = fields.UUIDField(pk=True)
    first_name = fields.CharField(max_length=100, null=False)
    last_name = fields.CharField(max_length=100, null=False)
    user_name = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    image_url = fields.CharField(max_length=100, null=True, unique=True)
    phone_number = fields.CharField(max_length=9, null=False)
    selected_exam = fields.JSONField(null=False)
    guardian_phone_number = fields.CharField(max_length=9, null=False)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)

user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "uuid", ))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude=("join_date", "uuid", "is_verified" ))
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password", ))
login_schema = pydantic_model_creator(User, name="LoginSchema", include=("email", "password"))
