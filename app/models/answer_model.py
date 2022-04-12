from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class Answer(Model):
    uuid = fields.UUIDField(pk=True)
    is_an_image = fields.BooleanField(default=False)
    image = fields.TextField()
    text = fields.CharField(max_length=100)
    letter = fields.CharField(max_length=3)
    is_correct = fields.BooleanField(default=False)
    question = fields.ForeignKeyField("models.Question", related_name="answers")

answer_pydantic = pydantic_model_creator(Answer, name="Topic", exclude=("uuid", ))
answer_pydanticIn = pydantic_model_creator(Answer, name="TopicIn", exclude=("uuid"))
answer_pydanticOut = pydantic_model_creator(Answer, name="TopicOut")