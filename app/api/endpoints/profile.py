from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.db.session import get_db_session
from app.schemas.user_schema import User
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.get('/profile/', status_code=200, response_model=User)
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db_session)
):
    return current_user
