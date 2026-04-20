from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_clickhouse_client
from app.models.user import CREATE_USERS_TABLE
from app.models.event import CREATE_EVENTS_TABLE
from app.router import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    client = await get_clickhouse_client()
    await client.command(CREATE_USERS_TABLE)
    await client.command(CREATE_EVENTS_TABLE)
    yield


app = FastAPI(title="Analytics Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
