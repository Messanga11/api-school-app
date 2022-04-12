from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class Topic(Model):
    uuid = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=100)
    subject_uuid = fields.CharField(max_length=100)
    subject = fields.ForeignKeyField("models.Subject", related_name="topics")
    visible_for= fields.CharField(max_length=3, null=False)

topic_pydantic = pydantic_model_creator(Topic, name="Topic", exclude=("uuid", ))
topic_pydanticIn = pydantic_model_creator(Topic, name="TopicIn", exclude=("uuid"))
topic_pydanticOut = pydantic_model_creator(Topic, name="TopicOut")