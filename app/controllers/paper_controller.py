import math
from typing import Any, Optional
from fastapi import APIRouter, Depends
from schema.app_schema import DataList
from schema.paper import PaperOutSchema
from models.answer_model import Answer
from models.subject_model import Subject
from models.question_model import question_pydanticOut
from controllers.auth_controller import get_current_user
from schema.paper import PaperInSchema
from tortoise.queryset import QuerySet

from auth import *
from models.paper_model import *


router = APIRouter(
    prefix="/administration/papers",
    tags=["papers"]
)


@router.post("", response_model=paper_pydanticOut)
async def create_paper(paper:PaperInSchema):
    
    paper_obj = paper.dict(exclude_unset=True,)

    paper_db = None

    subject = await Subject.get(uuid = paper_obj["subject_id"])

    if not subject:
        raise HTTPException(
            status_code=400,
            detail="Subject not exist"
        )

    paper_db = await Paper.create(
        subject_id=paper_obj["subject_id"],
        paper_type=paper_obj["paper_type"],
        visible_for=paper_obj["visible_for"],
        year=paper_obj["year"]
    )

    created_paper = await paper_pydanticOut.from_tortoise_orm(paper_db)

    # Question and answer creation
    for question_answer in paper_obj["questions"]:
        question = await Question.create(**question_answer["question"], paper_id=created_paper.dict()["uuid"])

        if question:
            created_question = await question_pydanticOut.from_tortoise_orm(question)
            for answer in question_answer["answers"]:
                await Answer.create(**answer, question_id = created_question.dict()["uuid"])
        else:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong!"
            )

    return await paper_pydanticOut.from_tortoise_orm(paper_db)

@router.get("", response_model=DataList)
async def papers(page:int=1, per_page:int=10):
    papers = await QuerySet(Paper)\
        .offset(per_page*(page-1))\
        .limit(per_page*(page-1) + per_page)\
        .values()

    for paper in papers:
        paper["questions"] = await QuerySet(Question).filter(paper_id = paper["uuid"]).values()

        if paper["questions"]:
            for question in paper["questions"]:
                question["answers"] = await QuerySet(Answer).filter(question_id = question["uuid"]).values()
    


    total = await QuerySet(Paper).count()
    return {
        'total': total,
        "data": papers,
        "current_page": page,
        "per_page": per_page,
        "pages":  math.ceil(total/len(papers)) if len(papers) != 0 else 0
    }

@router.get("/{subject_uuid}")
async def get_papers(subject_uuid: str):

    subject = Subject.get(uuid=subject_uuid)
    if not subject:
        raise HTTPException(
            status_code=422,
            detail="Subject not exist"
        )

    papers = await Topic.filter(subject_uuid=subject_uuid)
    return {
        "data": papers
    }

@router.get("/{id}")
async def get_paper(id: int):
    paper = await Topic.get(id=id)
    return paper


@router.put("")
async def update_paper(paper_in: paper_pydanticOut):
    paper_obj = paper_in.dict(exclude_unset=True)
    paper = await Topic.get(uuid=paper_obj["uuid"])
    if paper:
        paper_db = await paper.update_from_dict(paper_obj)
        await paper_db.save()
        await paper_db.refresh_from_db()
    return await paper_pydanticOut.from_tortoise_orm(paper_db)

@router.delete("/{paper_uuid}")
async def delete_paper(paper_uuid: str):
    paper_in = await Paper.get(uuid=paper_uuid)
    if paper_in:
        await paper_in.delete()
    
    return {
        "message": "Deleted"
    }