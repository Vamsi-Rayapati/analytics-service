from fastapi import APIRouter

from app.api.v1.router import router as v1_router

router = APIRouter(prefix="/analytics")


@router.get("/health")
async def health():
    return {"status": "ok"}


router.include_router(v1_router)
