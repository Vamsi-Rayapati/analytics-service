import uuid
from datetime import datetime, timezone
from typing import Any

from clickhouse_connect.driver.asyncclient import AsyncClient
from fastapi import HTTPException, status

from app.api.v1.events.schema import EventCreate
from app.models.event import Event

_COLS = (
    "id, event_name, app_build_number, app_release, app_version, "
    "app_version_string, brand, carrier, city, device_id, manufacturer, "
    "model, os, os_version, region, extra, created_at"
)
_INSERT_COLS = [
    "id", "event_name", "app_build_number", "app_release", "app_version",
    "app_version_string", "brand", "carrier", "city", "device_id",
    "manufacturer", "model", "os", "os_version", "region", "extra", "created_at",
]


def _row_to_event(row: tuple) -> Event:
    extra = row[15] if isinstance(row[15], dict) else {}
    return Event(
        id=row[0],
        event_name=row[1],
        app_build_number=row[2],
        app_release=row[3],
        app_version=row[4],
        app_version_string=row[5],
        brand=row[6],
        carrier=row[7],
        city=row[8],
        device_id=row[9],
        manufacturer=row[10],
        model=row[11],
        os=row[12],
        os_version=row[13],
        region=row[14],
        extra=extra,
        created_at=row[16],
    )


async def get_events_page(
    client: AsyncClient,
    limit: int = 20,
    cursor: str | None = None,
) -> tuple[list[Event], str | None]:
    if cursor:
        cursor_dt = datetime.fromisoformat(cursor)
        result = await client.query(
            f"SELECT {_COLS} FROM events "
            f"WHERE created_at < {{cursor:DateTime64(3, 'UTC')}} "
            f"ORDER BY created_at DESC LIMIT {{limit:UInt32}}",
            parameters={"cursor": cursor_dt, "limit": limit},
        )
    else:
        result = await client.query(
            f"SELECT {_COLS} FROM events ORDER BY created_at DESC LIMIT {{limit:UInt32}}",
            parameters={"limit": limit},
        )

    events = [_row_to_event(row) for row in result.result_rows]
    next_cursor = events[-1].created_at.isoformat() if len(events) == limit else None
    return events, next_cursor


async def get_event_by_id(event_id: str, client: AsyncClient) -> Event:
    result = await client.query(
        f"SELECT {_COLS} FROM events WHERE id = {{id:String}}",
        parameters={"id": event_id},
    )
    if not result.result_rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )
    return _row_to_event(result.result_rows[0])


async def create_event(payload: EventCreate, client: AsyncClient) -> Event:
    event_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    await client.insert(
        "events",
        [[
            event_id,
            payload.event_name,
            payload.app_build_number,
            payload.app_release,
            payload.app_version,
            payload.app_version_string,
            payload.brand,
            payload.carrier,
            payload.city,
            payload.device_id,
            payload.manufacturer,
            payload.model,
            payload.os,
            payload.os_version,
            payload.region,
            payload.extra or {},
            now,
        ]],
        column_names=_INSERT_COLS,
    )

    return Event(
        id=event_id,
        event_name=payload.event_name,
        app_build_number=payload.app_build_number,
        app_release=payload.app_release,
        app_version=payload.app_version,
        app_version_string=payload.app_version_string,
        brand=payload.brand,
        carrier=payload.carrier,
        city=payload.city,
        device_id=payload.device_id,
        manufacturer=payload.manufacturer,
        model=payload.model,
        os=payload.os,
        os_version=payload.os_version,
        region=payload.region,
        extra=payload.extra or {},
        created_at=now,
    )
