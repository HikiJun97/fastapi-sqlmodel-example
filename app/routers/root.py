from fastapi import APIRouter
from app.routers import users

router = APIRouter(
    prefix="/api",
)

router.include_router(users.router)
