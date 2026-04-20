from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id               String,
    event_name       String,
    app_build_number String,
    app_release      String,
    app_version      String,
    app_version_string String,
    brand            String,
    carrier          String,
    city             String,
    device_id        String,
    manufacturer     String,
    model            String,
    os               String,
    os_version       String,
    region           String,
    extra            JSON,
    created_at       DateTime64(3, 'UTC')
) ENGINE = MergeTree()
ORDER BY (event_name, created_at)
"""


@dataclass
class Event:
    id: str
    event_name: str
    app_build_number: str
    app_release: str
    app_version: str
    app_version_string: str
    brand: str
    carrier: str
    city: str
    device_id: str
    manufacturer: str
    model: str
    os: str
    os_version: str
    region: str
    extra: dict[str, Any]
    created_at: datetime
