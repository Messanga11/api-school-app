from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class Video(Model):
    id = fields.IntField(pk=True, index=True)
    uuid = fields.CharField(unique=True, default=uuid.uuid4(), max_length=100)
    title = fields.CharField(max_length=100)
    topic_uuid = fields.CharField(max_length=100)
    topic = fields.ForeignKeyField("models.Video", related_name="videos")

video_pydantic = pydantic_model_creator(Video, name="Video", exclude=("id", ))
video_pydanticIn = pydantic_model_creator(Video, name="Video", exclude_readonly=True)
video_pydanticOut = pydantic_model_creator(Video, name="Video", exclude=("id"))