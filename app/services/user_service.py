from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import models
from app.schemas.user_schema import User, UserCreate
from app.utils.helper import get_password_hash


async def create_user(user_schema: UserCreate, db: AsyncSession) -> User:

    hashed_password = await get_password_hash(user_schema.password)

    stmt_u_check = select(models.User).where(models.User.username == user_schema.username)
    stmt_e_check = select(models.User).where(models.User.email == user_schema.email)
    username = await db.execute(stmt_u_check)
    email = await db.execute(stmt_e_check)
    existing_username = username.scalar_one_or_none()
    existing_email = email.scalar_one_or_none()

    if existing_username or existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user already exist",
        )

    stmt = (
        insert(models.User)
        .values(
            username=user_schema.username,
            email=user_schema.email,
            password=hashed_password,
        )
        .returning(models.User)
    )

    result = await db.execute(stmt)
    await db.commit()
    new_user = result.scalar_one()
    return new_user


async def get_user(username: str, db: AsyncSession) -> User:
    stmt = select(models.User).where(models.User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {username} does not exist",
        )
    return user