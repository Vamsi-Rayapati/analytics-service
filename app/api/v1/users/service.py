from datetime import datetime, timezone

from fastapi import HTTPException, status
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.models.user import User
from app.api.v1.users.schema import UserCreate, UserUpdate

_COLS = "id, name, email, is_active, created_at, updated_at"
_INSERT_COLS = ["id", "name", "email", "is_active", "created_at", "updated_at"]


def _row_to_user(row: tuple) -> User:
    return User(
        id=row[0],
        name=row[1],
        email=row[2],
        is_active=bool(row[3]),
        created_at=row[4],
        updated_at=row[5],
    )


async def _next_id(client: AsyncClient) -> int:
    result = await client.query("SELECT max(id) FROM users")
    max_id = result.first_row[0]
    return (max_id or 0) + 1


async def get_all_users(client: AsyncClient) -> list[User]:
    result = await client.query(
        f"SELECT {_COLS} FROM users FINAL ORDER BY id"
    )
    return [_row_to_user(row) for row in result.result_rows]


async def get_user_by_id(user_id: int, client: AsyncClient) -> User:
    result = await client.query(
        f"SELECT {_COLS} FROM users FINAL WHERE id = {{id:UInt32}}",
        parameters={"id": user_id},
    )
    if not result.result_rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return _row_to_user(result.result_rows[0])


async def create_user(payload: UserCreate, client: AsyncClient) -> User:
    existing = await client.query(
        "SELECT id FROM users FINAL WHERE email = {email:String}",
        parameters={"email": payload.email},
    )
    if existing.result_rows:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{payload.email}' already exists",
        )

    user_id = await _next_id(client)
    now = datetime.now(timezone.utc)

    await client.insert(
        "users",
        [[user_id, payload.name, payload.email, 1, now, now]],
        column_names=_INSERT_COLS,
    )

    return User(
        id=user_id,
        name=payload.name,
        email=payload.email,
        is_active=True,
        created_at=now,
        updated_at=now,
    )


async def update_user(
    user_id: int, payload: UserUpdate, client: AsyncClient
) -> User:
    user = await get_user_by_id(user_id, client)

    if payload.email and payload.email != user.email:
        existing = await client.query(
            "SELECT id FROM users FINAL WHERE email = {email:String}",
            parameters={"email": payload.email},
        )
        if existing.result_rows:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' is already taken",
            )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc)

    await client.insert(
        "users",
        [[
            user.id, user.name, user.email,
            int(user.is_active), user.created_at, user.updated_at,
        ]],
        column_names=_INSERT_COLS,
    )

    return user


async def delete_user(user_id: int, client: AsyncClient) -> None:
    await get_user_by_id(user_id, client)
    await client.command(
        "DELETE FROM users WHERE id = {id:UInt32}",
        parameters={"id": user_id},
    )
