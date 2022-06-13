
#Enums
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

class FileModel(Model):
    uuid = fields.UUIDField(pk=True)
    title= fields.CharField(max_length=120)
    url= fields.CharField(max_length=100)
    type = fields.CharField(max_length=9)
    topic = fields.ForeignKeyField("models.Topic", related_name="files", null=True)

file_pydantic = pydantic_model_creator(FileModel, name="File", exclude=("uuid", ))
file_pydanticIn = pydantic_model_creator(FileModel, name="FileIn", exclude_readonly=True, exclude=("uuid", "url",))
file_pydanticOut = pydantic_model_creator(FileModel, name="FileOut")