from tortoise import Model, fields
from models.user_model import User
from models.topic_model import Topic
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class Subject(Model):
    uuid = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=200, null=False)
    topics: fields.ReverseRelation["Topic"]
    visible_for = fields.CharField(null=False, max_length=3)

subject_pydantic = pydantic_model_creator(Subject, name="Subject")
subject_pydanticIn = pydantic_model_creator(Subject, name="SubjectIn", exclude_readonly=True, exclude=("id", "uuid"))
subject_pydanticOut = pydantic_model_creator(Subject, name="SubjectOut")