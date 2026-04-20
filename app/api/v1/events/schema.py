from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EventCreate(BaseModel):
    event_name: str = Field(..., min_length=1, max_length=200, examples=["app_open"])
    app_build_number: str = Field(default="", examples=["3049"])
    app_release: str = Field(default="", examples=["3049"])
    app_version: str = Field(default="", examples=["3.0.49"])
    app_version_string: str = Field(default="", examples=["3.0.49"])
    brand: str = Field(default="", examples=["samsung"])
    carrier: str = Field(default="", examples=["JIO 4G"])
    city: str = Field(default="", examples=["Jodhpur"])
    device_id: str = Field(default="", examples=["14456923-e53e-4a0c-8dfa-d3c408de69e9"])
    manufacturer: str = Field(default="", examples=["samsung"])
    model: str = Field(default="", examples=["SM-A156E"])
    os: str = Field(default="", examples=["Android"])
    os_version: str = Field(default="", examples=["16"])
    region: str = Field(default="", examples=["Rajasthan"])
    extra: dict[str, Any] | None = Field(default=None, examples=[{"custom_key": "custom_value"}])

    @field_validator("event_name")
    @classmethod
    def event_name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("event_name must not be blank")
        return v.strip()


class EventResponse(BaseModel):
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

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    data: list[EventResponse]
    next_cursor: str | None
