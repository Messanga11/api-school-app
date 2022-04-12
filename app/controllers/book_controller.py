import base64
from fastapi import APIRouter, Depends, UploadFile
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
async def create_book(book: file_pydanticIn):
    
    book_obj = book.dict(exclude_unset=True)
    topic = Topic.get(uuid = book_obj["topic_uuid"])

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not exist"
        )
    
    url = create_file(base64)

    book_obj = await FileModel.create(**book_obj, topic_id=book_obj["topic_uuid"], url=url)

    new_book = await file_pydanticOut.from_tortoise_orm(book_obj)
    return new_book

@router.get("")
async def get_books():
    books = await file_pydanticOut.from_queryset(FileModel.all())
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