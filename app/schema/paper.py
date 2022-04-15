from typing import List, Optional
from .question import Question
from .answer import Answer
from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    uuid: Optional[str]
    question: Question
    answers: List[Answer]

class PaperInSchema(BaseModel):
    subject_id: str = None
    year: int = None
    paper_type: str = None
    visible_for: str = None
    questions: List[QuestionAnswer] = None
class PaperInUpdateSchema(BaseModel):
    uuid: str
    subject_id: str = None
    year: int = None
    paper_type: str = None
    visible_for: str = None
    questions: List[QuestionAnswer] = None


class AnswerForm(BaseModel):
    paper_uuid: str
    answers: List[str]

class PaperOutSchema(BaseModel):
    uuid: str
    subject_id: str = None
    year: int = None
    paper_type: str = None
    visible_for: str = None
    questions: List[QuestionAnswer]