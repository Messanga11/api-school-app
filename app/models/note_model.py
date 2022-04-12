import uuid
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Note(Model):
    uuid = fields.UUIDField(pk=True)
    url = fields.CharField(max_length=100, null=False)
    topic = fields.ForeignKeyField("models.Topic", related_name="notes")
    
note_pydantic = pydantic_model_creator(Note, name="Note", exclude=("uuid", ))
note_pydanticIn = pydantic_model_creator(Note, name="NoteIn", exclude_readonly=True)
note_pydanticOut = pydantic_model_creator(Note, name="NoteOut")