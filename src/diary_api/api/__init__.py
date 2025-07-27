from fastapi import APIRouter
from .routes import diary

api_router = APIRouter()
api_router.include_router(diary.router)