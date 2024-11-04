from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=True, poolclass=NullPool)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session():
    session = async_session()
    try:
        yield session
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail="Session error") from e
    finally:
        await session.close()
