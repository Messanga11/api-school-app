from core.settings import AppConfig
import secrets

from fastapi import File, UploadFile

async def create_file(file:UploadFile=File(...)):
    FILEPATH = "static/files/"
    filename = str(file.filename)
    extension = filename.split(".")[len(filename.split(".")) - 1]

    token_name = secrets.token_hex(10) + "." + extension

    generated_name = FILEPATH + token_name

    file_content = await file.read()

    with open(generated_name, "wb") as f:
        f.write(file_content)
    f.close()

    # with open(generated_name, "wb") as file:
    #     await file.write(file_content)
    
    # file.close()
    return generated_name



def get_image_full_url(url):
        return AppConfig.API_URL + str(url) if url else ""