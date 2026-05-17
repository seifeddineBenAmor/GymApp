from fastapi import APIRouter
from app.api.v1.endpoints import auth, categories, exercises

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
