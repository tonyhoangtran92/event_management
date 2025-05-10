from fastapi import APIRouter

from app.routers import fixture_data
from app.routers import user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(fixture_data.router, prefix="/fixture_data", tags=["fixture_data"])
