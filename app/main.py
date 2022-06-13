from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from controllers.router import api_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

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
    expose_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models" : ["models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)