from pydantic import BaseModel


class Country(BaseModel):
    country: str


class Genre(BaseModel):
    genre: str


class Movie(BaseModel):
    kinopoiskId: int | None = None
    kinopoiskHDId: str | None = None
    imdbId: str | None = None
    nameRu: str | None = None
    nameEn: str | None = None
    nameOriginal: str | None = None
    posterUrl: str | None = None
    posterUrlPreview: str | None = None
    coverUrl: str | None = None
    logoUrl: str | None = None
    reviewsCount: int | None = None
    ratingGoodReview: float | None = None
    ratingGoodReviewVoteCount: int | None = None
    ratingKinopoisk: float | None = None
    ratingKinopoiskVoteCount: int | None = None
    ratingImdb: float | None = None
    ratingImdbVoteCount: int | None = None
    ratingFilmCritics: float | None = None
    ratingFilmCriticsVoteCount: int | None = None
    ratingAwait: float | None = None
    ratingAwaitCount: int | None = None
    ratingRfCritics: float | None = None
    ratingRfCriticsVoteCount: int | None = None
    webUrl: str | None = None
    year: int | None = None
    filmLength: int | None = None
    slogan: str | None = None
    description: str | None = None
    shortDescription: str | None = None
    editorAnnotation: str | None = None
    isTicketsAvailable: bool | None = None
    productionStatus: str | None = None
    type: str | None = None
    ratingMpaa: str | None = None
    ratingAgeLimits: str | None = None
    hasImax: bool | None = None
    has3D: bool | None = None
    lastSync: str | None = None
    countries: list[Country] | None = []
    genres: list[Genre] | None = []
    startYear: int | None = None
    endYear: int | None = None
    serial: bool | None = None
    shortFilm: bool | None = None
    completed: bool | None = None

    class Config:
        populate_by_name = True


class Film(BaseModel):
    filmId: int | None = None
    nameRu: str | None = None
    nameEn: str | None = None
    type: str | None = None
    year: int | None = None
    description: str | None = None
    filmLength: str | None = None
    countries: list[Country] | None = []
    genres: list[Genre] | None = []
    rating: str | None = None
    ratingVoteCount: int | None = None
    posterUrl: str | None = None
    posterUrlPreview: str | None = None


class MovieSearchResults(BaseModel):
    keyword: str | None = None
    pagesCount: int | None = None
    searchFilmsCountResult: int | None = None
    films: list[Film]

    class Config:
        populate_by_name = True
