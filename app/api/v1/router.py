from fastapi import APIRouter

from app.api.v1.users.router import router as users_router
from app.api.v1.events.router import router as events_router

router = APIRouter(prefix="/api/v1")

router.include_router(users_router)
router.include_router(events_router)
