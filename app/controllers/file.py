import base64
from fileinput import filename
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
import secrets
from schema.file import ProfilePicIn
from utils import create_file
from models import User
from PIL import Image
# from schemas.user import user_pydantic

from controllers.auth_controller import get_current_user

router = APIRouter(tags=["files"], prefix="/upload")

@router.post("/images/update-profile")
async def upload_file(file:UploadFile=File(...), user=Depends(get_current_user)):
    FILEPATH = "static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="File extension not allowed",
            headers=["WWW-Authenticate", "Bearer"]
        )

    token_name = secrets.token_hex(10) + "." + "png"
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
    

    # Pillow
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()
    await user.update_from_dict({ "image_url": generated_name })
    await user.save()
    await user.refresh_from_db()

    return {
        "status": "ok"
    }

@router.post("/files")
async def upload_file(file:UploadFile=File(...)):
    await create_file(file)

    return {
        "status": "ok"
    }