from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.db.session import get_db_session
from app.schemas.user_schema import Token, User, UserCreate
from app.services.auth_service import login_for_access_token
from app.services.user_service import create_user

router = APIRouter()


@router.post('/register/', status_code=201, response_model=User)
async def register(user_schema: UserCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_user(user_schema=user_schema, db=db)


@router.post('/login/', status_code=200, response_model=Token)
async def login(
    # username: Annotated[str, Form()],
    # password: Annotated[str, Form()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db_session)
):
    return await login_for_access_token(form_data=form_data, db=db)