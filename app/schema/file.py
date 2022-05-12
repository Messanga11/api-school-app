from fastapi import File, UploadFile
from pydantic import BaseModel


class ProfilePicIn(BaseModel):
    base_64:str

class Base64Payload:
    base_64: str
    extension: str