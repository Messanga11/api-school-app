
#Enums
from enum import IntEnum
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class BookTypes(IntEnum):
    simple = 0
    library = 1

class Book(Model):
    uuid = fields.UUIDField(pk=True)
    title= fields.CharField(max_length=100)
    url= fields.CharField(max_length=100)
    topic_uuid = fields.CharField(max_length=100)
    topic = fields.ForeignKeyField("models.Topic", related_name="books")

book_pydantic = pydantic_model_creator(Book, name="Book", exclude=("uuid", ))
book_pydanticIn = pydantic_model_creator(Book, name="BookIn", exclude_readonly=True, exclude=("url"))
book_pydanticOut = pydantic_model_creator(Book, name="BookOut")