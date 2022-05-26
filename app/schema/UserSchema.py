from typing import Optional
from pydantic import BaseModel


class UserIn(BaseModel):
    uuid: Optional[str] = None
    first_name: str = None
    last_name: str = None
    user_name: str = None
    email: str = None
    gender: str
    exam: str
    phone_number: str = None
    selected_exam: str = None
    guardian_phone_number: str = None
    previous_password: Optional[str] = None
    password: str = None