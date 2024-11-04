from fastapi import HTTPException
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import models
from app.schemas.movie_schema import Movie, MovieSearchResults
from app.schemas.user_schema import User
from app.utils.kinopoisk_api import KINOPOISK

kinopoisk = KINOPOISK()


async def search_movie_by_title(query: str, page: int) -> MovieSearchResults:
    response_json = await kinopoisk.search(query=query, page=page)
    try:
        parsed_data = MovieSearchResults(**response_json)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail='Error parsing json data') from exc
    return parsed_data


async def get_movie_by_id(id: int) -> Movie:
    response_json = await kinopoisk.movie(id=id)
    try:
        parsed_data = Movie(**response_json)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail='Error parsing json data') from exc
    return parsed_data


async def add_favorite_movie(user: User, id: int, db: AsyncSession) -> Movie:

    check_mov_stmt = select(models.Movie).where(models.Movie.kinopoiskId == id)
    check_fav_stmt = select(models.Favorite).where(
        models.Favorite.user_id == user.id, models.Favorite.movie_id == id
    )
    result_mov = await db.execute(check_mov_stmt)
    result_fav = await db.execute(check_fav_stmt)
    movie = result_mov.scalar_one_or_none()
    liked = result_fav.scalar_one_or_none()
    if not movie:
        response_json = await kinopoisk.movie(id=id)
        try:
            parsed_data = Movie(**response_json)
        except ValueError as exc:
            raise HTTPException(
                status_code=500, detail='Error parsing json data'
            ) from exc
        mov_stmt = (
            insert(models.Movie).values(**parsed_data.dict()).returning(models.Movie)
        )

        result = await db.execute(mov_stmt)
        movie = result.scalar_one()

    if liked:
        raise HTTPException(status_code=400, detail='Movie already liked')
    fav_stmt = insert(models.Favorite).values(user_id=user.id, movie_id=id)
    await db.execute(fav_stmt)
    await db.commit()

    return movie


async def get_favorite_movies(user: User, db: AsyncSession) -> list[Movie]:
    favs_stmt = select(models.Favorite).where(models.Favorite.user_id == user.id)
    results = await db.execute(favs_stmt)
    favorites = results.scalars().all()
    detailed_movie = []

    for favorite in favorites:
        mov_stmt = select(models.Movie).where(models.Movie.kinopoiskId == favorite.movie_id)
        result = await db.execute(mov_stmt)
        detailed_movie.append(result.scalar_one())

    return detailed_movie


async def delete_favorite_movie(user: User, id: int, db: AsyncSession) -> None:

    check_mov_stmt = select(models.Movie).where(models.Movie.kinopoiskId == id)
    check_fav_stmt = select(models.Favorite).where(
        models.Favorite.user_id == user.id, models.Favorite.movie_id == id
    )
    result_mov = await db.execute(check_mov_stmt)
    result_fav = await db.execute(check_fav_stmt)
    movie = result_mov.scalar_one_or_none()
    liked = result_fav.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie doesn't exist")

    if not liked:
        raise HTTPException(status_code=400, detail='Movie not liked')
    fav_stmt = delete(models.Favorite).where(
        models.Favorite.user_id == user.id, models.Favorite.movie_id == id
    )
    await db.execute(fav_stmt)
    await db.commit()
