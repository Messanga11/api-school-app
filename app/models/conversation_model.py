from dataclasses import dataclass
from email import message
from typing import Any
from tortoise import fields
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from models.message_model import Message


class Conversation(Model):
    uuid = fields.UUIDField(pk=True)
    messages: fields.ReverseRelation[Message]
    members: fields.ManyToManyRelation[Any] = fields.ManyToManyField(
        "models.User", related_name="conversations", through="user_conversation"
    )
pydantic_conversation = pydantic_model_creator(
    Conversation,
    name="Conversation",
)
