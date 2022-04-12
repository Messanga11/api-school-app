from fileinput import filename
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
import secrets
from utils import create_file
from models import User
# from schemas.user import user_pydantic

# from controllers.auth import get_current_user

router = APIRouter(tags=["files"], prefix="/upload")

# from PIL import Image

@router.post("/images")
async def upload_file(file:UploadFile=File(...)):
    FILEPATH = "static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
    

    # Pillow
    # img = Image.open(generated_name)
    # img = img.resize(size=(200, 200))
    # img.save(generated_name)

    file.close()

    # user_db = await User.get(_id = user._id)

    # if(user_db):
    #     user_db.image = token_name
    #     await user_db.save()
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Cannot perform this action",
    #         headers=["WWW-Authenticate", "Bearer"]
    #     )
    return {
        "status": "Ok"
    }

@router.post("/images/update-profile")
async def upload_file(file:UploadFile=File(...)):
    FILEPATH = "static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
    

    # Pillow
    # img = Image.open(generated_name)
    # img = img.resize(size=(200, 200))
    # img.save(generated_name)

    file.close()

    # user_db = await User.get(_id = user._id)

    # if(user_db):
    #     user_db.image = token_name
    #     await user_db.save()
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Cannot perform this action",
    #         headers=["WWW-Authenticate", "Bearer"]
    #     )
    return {
        "status": "Ok"
    }

@router.post("/files")
async def upload_file(file:UploadFile=File(...)):
    create_file(file)

    return {
        "status": "ok"
    }