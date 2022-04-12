from fastapi import APIRouter, Depends
from controllers.auth_controller import get_current_user

from auth import *
from models.note_model import *


router = APIRouter(
    prefix="/administration/notes",
    tags=["notes"]
)


@router.post("/")
async def create_note(note: note_pydanticIn, user = Depends(get_current_user)):
    note_obj = note.dict(exclude_unset=True)
    note_obj = await Note.create(**note_obj)
    new_note = await note_pydantic.from_tortoise_orm(note_obj)
    return new_note

@router.get("/")
async def get_notes():
    notes = await Note.all()
    return notes

@router.get("/{id}")
async def get_notes(id: int):
    note = await Note.get(id=id)
    return note

@router.put("/{id}")
async def get_notes(id: int, note_in: note_pydanticIn):
    note = await Note.get(id=id)
    if note:
        note_db = await note.update_from_dict(note_in)
        note_db.save()
    return await note_pydanticOut.from_tortoise_orm(note_in)

@router.delete("/{id}")
async def delete_note(id: int):
    note_in = await Note.get(id=id)
    if note_in:
        await note_in.delete()
    
    return {
        "message": "Deleted"
    }