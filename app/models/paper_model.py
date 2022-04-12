from tortoise import Model, fields
from .question_model import Question
from models.user_model import User
from models.topic_model import Topic
from tortoise.contrib.pydantic import pydantic_model_creator

class Paper(Model):
    uuid = fields.UUIDField(pk=True)
    subject = fields.ForeignKeyField("models.Subject", related_name="papers")
    year = fields.IntField(null=False)
    paper_type = fields.CharField(max_length=200, null=False)
    visible_for = fields.CharField(null=False, max_length=3)
    questions = fields.ReverseRelation["Question"]

paper_pydantic = pydantic_model_creator(Paper, name="Paper")
paper_pydanticIn = pydantic_model_creator(Paper, name="PaperIn", exclude_readonly=True, exclude=("id", "uuid"))
paper_pydanticOut = pydantic_model_creator(Paper, name="PaperOut")