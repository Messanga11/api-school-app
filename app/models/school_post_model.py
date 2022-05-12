
from tortoise import Model, fields
from .school_model import School
from tortoise.contrib.pydantic import pydantic_model_creator

class SchoolPost(Model):
    uuid = fields.UUIDField(pk=True)
    school = fields.ForeignKeyField("models.School", related_name="posts")
    title = fields.CharField(max_length=200)
    description = fields.TextField()
    image_url = fields.CharField(max_length=100, null=True)
    base_64 = fields.TextField(null=True)
    
school_post_pydantic = pydantic_model_creator(SchoolPost, name="SchoolPost")
school_post_pydanticIn = pydantic_model_creator(SchoolPost, name="SchoolPostIn", exclude_readonly=True, exclude=("uuid"))
school_post_pydanticOut = pydantic_model_creator(SchoolPost, name="SchoolPostOut")