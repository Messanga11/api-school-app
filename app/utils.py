import base64
from schema.file import Base64Payload
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
        return (AppConfig.API_URL + str(url)) if url else ""
    
def save_base64(payload:Base64Payload):
    FILEPATH = "static/files/"
    extension = payload.extension

    token_name = secrets.token_hex(10) + "." + extension

    generated_name = FILEPATH + token_name

    file_as_bytes = str.encode(payload.filedata) # Convert str to bytes
    file_content = base64.b64decode(file_as_bytes) # decode base 64 string

    with open(generated_name, "wb") as f:
        f.write(file_content)
    f.close()

    # with open(generated_name, "wb") as file:
    #     await file.write(file_content)
    
    # file.close()
    return generated_name