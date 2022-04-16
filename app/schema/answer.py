from pydantic import BaseModel


class Answer(BaseModel):
    is_an_image: bool
    is_correct: bool
    image: str
    text: str
    letter: str