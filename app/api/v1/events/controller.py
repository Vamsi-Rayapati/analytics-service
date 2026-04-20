from fastapi import Depends, Query, Response, status
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.database import get_db
from app.api.v1.events.schema import EventCreate, EventListResponse, EventResponse
from app.api.v1.events import service


async def list_events(
    cursor: str | None = Query(default=None),
    db: AsyncClient = Depends(get_db),
) -> EventListResponse:
    events, next_cursor = await service.get_events_page(db, limit=20, cursor=cursor)
    return EventListResponse(
        data=[EventResponse.model_validate(e.__dict__) for e in events],
        next_cursor=next_cursor,
    )


async def get_event(
    event_id: str, db: AsyncClient = Depends(get_db)
) -> EventResponse:
    event = await service.get_event_by_id(event_id, db)
    return EventResponse.model_validate(event.__dict__)


async def create_event(
    payload: EventCreate,
    response: Response,
    db: AsyncClient = Depends(get_db),
) -> EventResponse:
    event = await service.create_event(payload, db)
    response.status_code = status.HTTP_201_CREATED
    return EventResponse.model_validate(event.__dict__)
