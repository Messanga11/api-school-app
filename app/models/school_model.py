
from dataclasses import dataclass
from email.policy import default
from enum import unique
from tortoise import Model, fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from core.settings import AppConfig


class School(Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    region = fields.CharField(max_length=100, null=False)
    email = fields.CharField(max_length=100, null=False)
    password = fields.CharField(max_length=100, null=False)
    type = fields.CharField(max_length=100, null=False, default="SCHOOL")
    principal = fields.JSONField(default={}, null=True)
    vice_principals = fields.JSONField(default=[], null=True)
    logo = fields.TextField(null=True)
    teachers = fields.JSONField(default=[], null=True)

school_pydantic = pydantic_model_creator(School, name="School", exclude=("is_verified", "uuid", ))
school_pydanticIn = pydantic_model_creator(School, name="SchoolIn", exclude=("uuid"))
school_pydanticOut = pydantic_model_creator(School, name="SchoolOut", exclude=("password", ))