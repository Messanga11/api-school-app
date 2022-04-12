import secrets

from fastapi import File, UploadFile


async def create_file(file:UploadFile=File(...)):
    FILEPATH = "static/files/"
    filename = file.filename
    extension = filename.split(".")[len(file.split(".")) - 1]

    token_name = secrets.token_hex(10) + "." + extension

    generated_name = FILEPATH + token_name

    file_content = await file.read()

    f = open(generated_name, "a")
    await f.write(file_content)
    await f.close()

    # with open(generated_name, "wb") as file:
    #     await file.write(file_content)
    
    # file.close()
    return generated_name