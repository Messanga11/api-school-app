import base64
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from utils import get_image_full_url
from controllers.auth_controller import get_current_user

from auth import *
from models.file_model import *
from models.topic_model import Topic
from utils import create_file


router = APIRouter(
    prefix="/administration/books",
    tags=["books"]
)


@router.post("")
async def create_book(title=Form(...), type=Form(...), topic_uuid=Form(...), file:UploadFile=File(...)):
    
    if not type in ["lib_book", "book", "video", "note", "video_vip"]:
        raise HTTPException(status_code=400, detail="Invalid type")

    if type != "lib_book" and topic_uuid == "nothing":
        raise HTTPException(status_code=422, detail="Fill all fields")
        
    
    book_obj = {
        "title": title,
        "type": type,
        "topic_uuid": None if topic_uuid == "nothing" else topic_uuid,
    }
    
    if not type == "lib_book":
        topic = await Topic.get(uuid = book_obj["topic_uuid"])

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="Topic not exist"
            )
    
    url = await create_file(file)

    book_obj = await FileModel.create(**book_obj, topic_id=book_obj["topic_uuid"], url=url)

    new_book = await file_pydanticOut.from_tortoise_orm(book_obj)
    return new_book

@router.get("")
async def get_books(type:str = None, current_user:User=Depends(get_current_user)):
        
    if type == None:
        if current_user.role != AppConfig.AppRoles.SUPER_ADMIN:
            # raise HTTPException(status_code=401, detail="Invalid params")
            pass
        else:
            return {
                "data": await FileModel.all()
            }
            
    
    if not type in ["lib_book", "book", "video", "note", "video_vip"]:
        raise HTTPException(status_code=400, detail="Invalid type")
    
    
    else:
        books = await FileModel.filter(type=type).all()
    
        for book in books:
            book.url = get_image_full_url(book.url)
        
        return {
            "data": books
        }

@router.get("/{topic_uuid}")
async def get_books(topic_uuid:str):
    books = await FileModel.filter(topic_uuid=topic_uuid)
    return {
        "data": books
    }

@router.get("/{id}")
async def get_books(id: int):
    book = await FileModel.get(id=id)
    return book

@router.put("/{id}")
async def get_books(id: int, book_in: file_pydanticIn):
    book = await FileModel.get(id=id)
    if book:
        book_db = await book.update_from_dict(book_in)
        book_db.save()
    return await file_pydanticOut.from_tortoise_orm(book_in)


@router.delete("/{book_uuid}")
async def delete_book(book_uuid: str):
    book_in = await FileModel.get(uuid=book_uuid)
    if book_in:
        await book_in.delete()
    
    return {
        "message": "Deleted"
    }