
from enum import unique
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Message(Model):
    uuid = fields.UUIDField(pk=True)
    conversation = fields.ForeignKeyField("models.Conversation", related_name="messages")
    text = fields.TextField()
    receiver = fields.ForeignKeyField("models.User", related_name="messages", null=True)
    receiver_guardian = fields.ForeignKeyField("models.Guardian", related_name="messages", null=True)
    sender_uuid = fields.CharField(max_length=100, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    

message_pydantic = pydantic_model_creator(Message, name="Message", exclude=("is_verified", "uuid", ))
message_pydanticIn = pydantic_model_creator(Message, name="MessageIn", exclude=("join_date", "uuid", "is_verified", "id", "created_at" ))
message_pydanticOut = pydantic_model_creator(Message, name="MessageOut", exclude_readonly=False,)