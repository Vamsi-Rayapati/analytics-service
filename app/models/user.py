from dataclasses import dataclass
from datetime import datetime

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id         UInt32,
    name       String,
    email      String,
    is_active  UInt8,
    created_at DateTime64(3, 'UTC'),
    updated_at DateTime64(3, 'UTC')
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY id
"""


@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
