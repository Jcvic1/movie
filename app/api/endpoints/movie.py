from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.db.session import get_db_session
from app.schemas.movie_schema import Movie, MovieSearchResults
from app.schemas.user_schema import User
from app.services.auth_service import get_current_active_user
from app.services.movie_service import (
    add_favorite_movie,
    delete_favorite_movie,
    get_favorite_movies,
    get_movie_by_id,
    search_movie_by_title,
)

router = APIRouter()


@router.get('/movies/search/', status_code=200, response_model=MovieSearchResults)
async def search_movie(
    current_user: Annotated[User, Depends(get_current_active_user)],
    query: str = '',
    page: int = Query(1, ge=1),
):
    return await search_movie_by_title(query=query, page=page)


@router.get('/movies/{kinopoisk_id}', status_code=200, response_model=Movie)
async def get_movie(
    current_user: Annotated[User, Depends(get_current_active_user)],
    kinopoisk_id: int
):
    return await get_movie_by_id(id=kinopoisk_id)


@router.get('/movies/favorites/', status_code=200, response_model=list[Movie])
async def get_favorites(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db_session),
):
    return await get_favorite_movies(user=current_user, db=db)


@router.post('/movies/favorites/{kinopoisk_id}', status_code=201, response_model=Movie)
async def add_favorite(
    current_user: Annotated[User, Depends(get_current_active_user)],
    kinopoisk_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    return await add_favorite_movie(user=current_user, id=kinopoisk_id, db=db)


@router.delete('/movies/favorites/{kinopoisk_id}', status_code=204)
async def delete_favorite(
    current_user: Annotated[User, Depends(get_current_active_user)],
    kinopoisk_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    return await delete_favorite_movie(user=current_user, id=kinopoisk_id, db=db)
