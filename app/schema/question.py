from pydantic import BaseModel


class Question(BaseModel):
    is_an_image: bool
    image: str
    text: str