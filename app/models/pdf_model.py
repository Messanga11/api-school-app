
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class PDF(Model):
    id = fields.IntField(pk=True, index=True)
    uuid = fields.UUIDField()
    title = fields.ForeignKeyField("models.Topic", related_name="pdfs")
    
pdf_pydantic = pydantic_model_creator(PDF, name="PDF", exclude=("uuid", ))
pdf_pydanticIn = pydantic_model_creator(PDF, name="PDFIn", exclude_readonly=True)
pdf_pydanticOut = pydantic_model_creator(PDF, name="PDFOut")