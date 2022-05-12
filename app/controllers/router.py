from fastapi import APIRouter
from .auth_controller import router as auth
from .subject_controller import router as subject
from .book_controller import router as books
from .note_controller import router as note
from .topic_controller import router as topic
from .video_controller import router as video
from .user_controller import router as user
from .student_controller import router as student
from .school_controller import router as school
from .school_post_controller import router as school_post
from .message_controller import router as message
from .paper_controller import router as paper
from .file import router as files

api_router = APIRouter()

api_router.include_router(auth)
api_router.include_router(paper)
api_router.include_router(student)
api_router.include_router(user)
api_router.include_router(books)
api_router.include_router(note)
api_router.include_router(topic)
api_router.include_router(video)
api_router.include_router(subject)
api_router.include_router(message)
api_router.include_router(files)
api_router.include_router(school)
api_router.include_router(school_post)