from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, recipe


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(recipe.router, prefix="/recipes", tags=["Recipes"])
