from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.api.v1.users.schema import UserCreate, UserUpdate


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.id))
    return list(result.scalars().all())


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


async def create_user(payload: UserCreate, db: AsyncSession) -> User:
    existing = await db.execute(
        select(User).where(User.email == payload.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{payload.email}' already exists",
        )
    user = User(name=payload.name, email=payload.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    user_id: int, payload: UserUpdate, db: AsyncSession
) -> User:
    user = await get_user_by_id(user_id, db)

    if payload.email and payload.email != user.email:
        existing = await db.execute(
            select(User).where(User.email == payload.email)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' is already taken",
            )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> None:
    user = await get_user_by_id(user_id, db)
    await db.delete(user)
    await db.commit()
