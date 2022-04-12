from typing import List
from .question import Question
from .answer import Answer
from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    question: Question
    answers: List[Answer]

class PaperInSchema(BaseModel):
    subject_id: str = None
    year: int = None
    paper_type: str = None
    visible_for: str = None
    questions: List[QuestionAnswer] = None

class PaperOutSchema(BaseModel):
    uuid: str
    subject_id: str = None
    year: int = None
    paper_type: str = None
    visible_for: str = None
    questions: List[QuestionAnswer]