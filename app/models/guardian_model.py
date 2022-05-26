from tortoise import Model, fields
import uuid
from tortoise.contrib.pydantic import pydantic_model_creator

class Guardian(Model):
    uuid = fields.UUIDField(pk=True)
    phone_number = fields.CharField(max_length=9, null=False, unique=True)
    
    def __repr__(self) -> str:
        return f"<Guardian uuid:{self.uuid} phone_number:{self.phone_number} />"

guardian_pydantic = pydantic_model_creator(Guardian, name="Guardian", exclude=("uuid", ))
guardian_pydanticIn = pydantic_model_creator(Guardian, name="GuardianIn", exclude_readonly=True)
guardian_pydanticOut = pydantic_model_creator(Guardian, name="GuardianOut")