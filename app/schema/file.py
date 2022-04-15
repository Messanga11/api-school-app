from fastapi import File, UploadFile
from pydantic import BaseModel


class ProfilePicIn(BaseModel):
    base_64:str