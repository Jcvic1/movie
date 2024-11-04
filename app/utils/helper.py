from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def kinopoisk_error(value):
    match value:
        case 401:
            raise HTTPException(
                status_code=value,
                detail='Пустой или неправильный токен',
            )
        case 402:
            raise HTTPException(
                status_code=value,
                detail='Превышен лимит запросов(или дневной, или общий)',
            )
        case 404:
            raise HTTPException(
                status_code=value,
                detail='Фильм не найден',
            )
        case 429:
            raise HTTPException(
                status_code=value,
                detail='Слишком много запросов. Общий лимит - 20 запросов в секунду',
            )
