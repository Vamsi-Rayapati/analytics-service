from fastapi import Depends, Response, status
from clickhouse_connect.driver.asyncclient import AsyncClient

from app.database import get_db
from app.api.v1.users.schema import UserCreate, UserResponse, UserUpdate
from app.api.v1.users import service


async def list_users(db: AsyncClient = Depends(get_db)) -> list[UserResponse]:
    users = await service.get_all_users(db)
    return [UserResponse.model_validate(u) for u in users]


async def get_user(
    user_id: int, db: AsyncClient = Depends(get_db)
) -> UserResponse:
    user = await service.get_user_by_id(user_id, db)
    return UserResponse.model_validate(user)


async def create_user(
    payload: UserCreate,
    response: Response,
    db: AsyncClient = Depends(get_db),
) -> UserResponse:
    user = await service.create_user(payload, db)
    response.status_code = status.HTTP_201_CREATED
    return UserResponse.model_validate(user)


async def update_user(
    user_id: int, payload: UserUpdate, db: AsyncClient = Depends(get_db)
) -> UserResponse:
    user = await service.update_user(user_id, payload, db)
    return UserResponse.model_validate(user)


async def delete_user(
    user_id: int,
    response: Response,
    db: AsyncClient = Depends(get_db),
) -> None:
    await service.delete_user(user_id, db)
    response.status_code = status.HTTP_204_NO_CONTENT
