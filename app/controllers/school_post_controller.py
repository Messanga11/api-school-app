import math
from multiprocessing.dummy import Array
from typing import Any, Optional
from fastapi import APIRouter, Depends
from schema.app_schema import DataList
from models.school_post_model import *
from models.subject_model import Subject
from models.question_model import question_pydanticOut
from controllers.auth_controller import get_current_user
from tortoise.queryset import QuerySet

from auth import *
from models.school_post_model import *


router = APIRouter(
    prefix="/administration/school_posts",
    tags=["school_posts"]
)


@router.post("", response_model=school_post_pydanticOut)
async def create_school_post(school_post:school_post_pydanticIn, current_school=Depends(get_current_user)):
    
    school_post_obj = school_post.dict(exclude_unset=True)
    school_post_db = await SchoolPost.create(**school_post_obj, school_id=current_school.uuid)
 
    return await school_post_pydanticOut.from_tortoise_orm(school_post_db)

@router.get("", response_model=DataList)
async def school_posts(page:int=1, per_page:int=100, keyword:Optional[str]=None, school_uuid:str=None):
    query_set = QuerySet(SchoolPost)
    
    if not school_uuid:
        raise HTTPException(
            status_code=404,
            detail="School not found"
        )
    else:
        school = await School.get_or_none(uuid=school_uuid)
        if not school:
            raise HTTPException(
                status_code=404,
                detail="School not found"
            )
    
    if keyword:
        query_set.filter(name__icontains=f"'{keyword}'")
    
    total = await QuerySet(SchoolPost).count()
    
    query_set = query_set\
        .offset(per_page*(page-1))\
        .limit(per_page)

    school_posts = await query_set.all()

    
    return {
        'total': total,
        "data": school_posts,
        "current_page": page,
        "per_page": per_page,
        "pages":  math.ceil(total/per_page) if per_page != 0 else 0
    }

@router.get("/{school_post_uuid}")
async def get_school_posts(school_post_uuid: str):

    school_post = await SchoolPost.filter(uuid=school_post_uuid).first()
    if not school_post:
        raise HTTPException(
            status_code=404,
            detail="SchoolPost not exist"
        )
    return school_post


@router.put("")
async def update_school_post(school_post: school_post_pydanticOut):
    
    school_post_obj = school_post.dict(exclude_unset=True,)

    school_post_db = await SchoolPost.get(uuid=school_post_obj["uuid"])

    school_post_db = await school_post_db.update_from_dict(school_post_obj)
    await school_post_db.save()
    await school_post_db.refresh_from_db()

    return await school_post_pydanticOut.from_tortoise_orm(school_post_db)

@router.delete("/{school_post_uuid}")
async def delete_school_post(school_post_uuid: str):
    school_post_in = await SchoolPost.get(uuid=school_post_uuid)
    if school_post_in:
        await school_post_in.delete()
    
    return {
        "message": "Deleted"
    }