from fileinput import filename
from turtle import title
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from utils import create_file
from controllers.auth_controller import get_current_user

from auth import *
from models.subject_model import *
from models.book_model import *
from models.topic_model import *
from models.video_model import *


router = APIRouter(
    prefix="/administration/subjects",
    tags=["subject"]
)


@router.post("", response_model=subject_pydanticOut)
async def create_subject(subject: subject_pydanticIn,):

    subject_obj = subject.dict(exclude_unset=True)
    subject_obj = await Subject.create(**subject_obj)

    new_subject = await subject_pydanticOut.from_tortoise_orm(subject_obj)
    return new_subject

@router.get("")
async def get_subjects(type:str, current_user:User = Depends(get_current_user)):
    subjects = []
    # if current_user.role == AppConfig.AppRoles.SUPER_ADMIN:
    if type:
        subjects = await subject_pydanticOut.from_queryset(Subject.filter(visible_for=type).all())
    # if current_user.role != AppConfig.AppRoles.STUDENT:
    else:
        subjects = await subject_pydanticOut.from_queryset(Subject.all())
        
    return {
        "data": subjects
    }

@router.get("/{id}")
async def get_subjects(id: int):
    subject = await Subject.get(id=id)
    return subject

@router.put("")
async def update_subject(subject_in: subject_pydanticOut):
    subject_obj = subject_in.dict(exclude_unset=True)
    subject = await Subject.get(uuid=subject_obj["uuid"])
    if subject:
        subject_db = await subject.update_from_dict(subject_obj)
        await subject_db.save()
        await subject_db.refresh_from_db()
    return await subject_pydanticOut.from_tortoise_orm(subject_db)

@router.delete("/{subject_uuid}")
async def delete_subject(subject_uuid: str):
    subject_in = await Subject.get(uuid=subject_uuid)
    if subject_in:
        await subject_in.delete()
    
    return {
        "message": "Deleted"
    }