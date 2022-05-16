import math
from multiprocessing.dummy import Array
from typing import Any, Optional
from fastapi import APIRouter, Depends
from schema.app_schema import DataList
from models.school_model import *
from models.subject_model import Subject
from models.question_model import question_pydanticOut
from controllers.auth_controller import get_current_user
from tortoise.queryset import QuerySet
from schema.school_schema import SchoolUpdateIn

from auth import *
from models.school_model import *


router = APIRouter(
    prefix="/administration/schools",
    tags=["schools"]
)


@router.post("", response_model=school_pydanticOut)
async def create_school(school:school_pydanticIn):
    
    school_obj = school.dict(exclude_unset=True)
    hashed_password = get_hashed_password(school_obj["password"])
    
    school_obj["password"] = hashed_password

    school_db = await School.create(**school_obj)
 
    return await school_pydanticOut.from_tortoise_orm(school_db)

@router.get("", response_model=DataList)
async def schools(page:int=1, per_page:int=10, keyword:Optional[str]=None, type:str="SCHOOL", region:Optional[str]=None):
    query_set = QuerySet(School)
    
    if type:
        query_set = query_set.filter(type=type)
    
    if keyword:
        query_set = query_set.filter(name__icontains=f"{keyword}")
    
    if region:
        query_set = query_set.filter(region__iexact=f"{region}")
    
    total = await query_set.count()
    
    query_set = query_set\
        .offset(per_page*(page-1))\
        .limit(per_page)

    data = await query_set.all()

    
    return {
        'total': total,
        "data": data,
        "current_page": page,
        "per_page": per_page,
        "pages":  math.ceil(total/per_page) if per_page != 0 else 0
    }

@router.get("/{school_uuid}")
async def get_schools(school_uuid: str):

    school = await School.filter(uuid=school_uuid).first()
    if not school:
        raise HTTPException(
            status_code=404,
            detail="School not exist"
        )
    return school


@router.put("")
async def update_school(school: SchoolUpdateIn, current_school=Depends(get_current_user)):
    
    school_obj = school.dict(exclude_unset=True)
    

    school_db = await School.get(uuid=school_obj["uuid"])

    if "previous_passord" in school_obj:
        if(not await verify_password(school_obj["previous_password"], school_db.password)):
            raise HTTPException(
                status_code=404,
                detail="Invalid previous password"
            )
    
        hash = get_hashed_password(school_obj["password"])
        school_obj["password"] = hash
        school_obj.pop("previous_password", None)

    school_db = await school_db.update_from_dict(school_obj)
    await school_db.save()
    await school_db.refresh_from_db()

    return await school_pydanticOut.from_tortoise_orm(school_db)

@router.delete("/{school_uuid}")
async def delete_school(school_uuid: str):
    school_in = await School.get(uuid=school_uuid)
    if school_in:
        await school_in.delete()
    
    return {
        "message": "Deleted"
    }