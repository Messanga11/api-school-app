from pydantic import BaseModel


class Answer(BaseModel):
    is_an_image: bool
    image: str
    text: str
    letter: str