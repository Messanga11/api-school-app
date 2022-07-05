from posixpath import dirname
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, Request
from controllers.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sse_starlette.sse import EventSourceResponse
from sh import tail
import time
import os

app = FastAPI()

app.include_router(api_router)
# i18n
# app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_language_header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = f"{dir_path}/test.log"
#This async generator will listen to our log file in an infinite while loop (happens in the tail command)
#Anytime the generator detects a new line in the log file, it will yield it.
async def logGenerator(request):
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line
        time.sleep(0.5)

#This is our api endpoint. When a client subscribes to this endpoint, they will recieve SSE from our log file
# @app.get('/stream-logs')
# async def runStatus(request: Request):
#     event_generator = logGenerator(request)
#     return EventSourceResponse(event_generator)

from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024*1024
video_path = Path("static/files/00c22d8e76d405b889e7.mp4")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.htm", context={"request": request})


@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")

app.mount("/static", StaticFiles(directory="static"), name="static")

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models" : ["models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)