from tortoise import Model, fields
from .answer_model import Answer
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class Question(Model):
    uuid = fields.UUIDField(pk=True)
    is_an_image = fields.BooleanField(default=False)
    image = fields.TextField()
    text = fields.CharField(max_length=100)
    paper = fields.ForeignKeyField("models.Paper", related_name="questions")
    answers: fields.ReverseRelation[Answer]

question_pydantic = pydantic_model_creator(Question, name="Question", exclude=("uuid", ))
question_pydanticIn = pydantic_model_creator(Question, name="QuestionIn", exclude=("uuid"))
question_pydanticOut = pydantic_model_creator(Question, name="QuestionOut")