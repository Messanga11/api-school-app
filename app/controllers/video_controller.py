from fastapi import APIRouter, Depends
from controllers.auth_controller import get_current_user

from auth import *
from models.video_model import *


router = APIRouter(
    prefix="/administration/videos",
    tags=["videos"]
)


@router.post("/")
async def create_video(video: video_pydanticIn, user = Depends(get_current_user)):
    video_obj = video.dict(exclude_unset=True)
    video_obj = await Video.create(**video_obj)
    new_video = await video_pydantic.from_tortoise_orm(video_obj)
    return new_video

@router.get("/")
async def get_videos():
    videos = await Video.all()
    return videos

@router.get("/{id}")
async def get_videos(id: int):
    video = await Video.get(id=id)
    return video

@router.put("/{id}")
async def get_videos(id: int, video_in: video_pydanticIn):
    video = await Video.get(id=id)
    if video:
        video_db = await video.update_from_dict(video_in)
        video_db.save()
    return await video_pydanticOut.from_tortoise_orm(video_in)

@router.delete("/{id}")
async def delete_video(id: int):
    video_in = await Video.get(id=id)
    if video_in:
        await video_in.delete()
    
    return {
        "message": "Deleted"
    }