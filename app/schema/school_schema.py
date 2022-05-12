from typing import Optional
from pydantic import BaseModel
from models.school_model import *

class SchoolUpdateIn(school_pydanticOut):
    previous_password: Optional[str] = None
    password: Optional[str] = None