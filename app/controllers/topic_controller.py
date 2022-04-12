from typing import Any, Optional
from fastapi import APIRouter, Depends
from models.subject_model import Subject
from controllers.auth_controller import get_current_user

from auth import *
from models.topic_model import *


router = APIRouter(
    prefix="/administration/topics",
    tags=["topics"]
)


@router.post("", response_model=topic_pydanticOut)
async def create_topic(topic:topic_pydanticIn):
    
    topic_obj = topic.dict(exclude_unset=True)

    subject = Subject.get(uuid = topic_obj["subject_uuid"])

    if not subject:
        raise HTTPException(
            status_code=400,
            detail="Subject not exist"
        )

    topic_obj = await Topic.create(**topic_obj, subject_id=topic_obj["subject_uuid"])
    
    new_topic = await topic_pydanticOut.from_tortoise_orm(topic_obj)
    return new_topic

@router.get("")
async def topics():
    topics = await topic_pydanticOut.from_queryset(Topic.all())
    return {
        "data": topics
    }

@router.get("/{subject_uuid}")
async def get_topics(subject_uuid: str):

    subject = Subject.get(uuid=subject_uuid)
    if not subject:
        raise HTTPException(
            status_code=422,
            detail="Subject not exist"
        )

    topics = await Topic.filter(subject_uuid=subject_uuid)
    return {
        "data": topics
    }

@router.get("/{id}")
async def get_topic(id: int):
    topic = await Topic.get(id=id)
    return topic


@router.put("")
async def update_topic(topic_in: topic_pydanticOut):
    topic_obj = topic_in.dict(exclude_unset=True)
    topic = await Topic.get(uuid=topic_obj["uuid"])
    if topic:
        topic_db = await topic.update_from_dict(topic_obj)
        await topic_db.save()
        await topic_db.refresh_from_db()
    return await topic_pydanticOut.from_tortoise_orm(topic_db)

@router.delete("/{topic_uuid}")
async def delete_topic(topic_uuid: str):
    topic_in = await Topic.get(uuid=topic_uuid)
    if topic_in:
        await topic_in.delete()
    
    return {
        "message": "Deleted"
    }