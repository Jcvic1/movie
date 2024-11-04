from sqlalchemy import ARRAY, JSON, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Favorite(Base):  # type: ignore
    __tablename__ = 'favorites'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.kinopoiskId'), primary_key=True)

    user = relationship('User', back_populates='favorite_movies')
    movie = relationship('Movie', back_populates='favorited_by')


class User(Base):  # type: ignore
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    favorite_movies = relationship(
        'Favorite', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active}>"


class Movie(Base):  # type: ignore
    __tablename__ = 'movies'

    kinopoiskId = Column(Integer, primary_key=True, index=True)
    kinopoiskHDId = Column(String)
    imdbId = Column(String)
    nameRu = Column(String)
    nameEn = Column(String)
    nameOriginal = Column(String)
    posterUrl = Column(String)
    posterUrlPreview = Column(String)
    coverUrl = Column(String)
    logoUrl = Column(String)
    reviewsCount = Column(Integer)
    ratingGoodReview = Column(Float)
    ratingGoodReviewVoteCount = Column(Integer)
    ratingKinopoisk = Column(Float)
    ratingKinopoiskVoteCount = Column(Integer)
    ratingImdb = Column(Float)
    ratingImdbVoteCount = Column(Integer)
    ratingFilmCritics = Column(Float)
    ratingFilmCriticsVoteCount = Column(Integer)
    ratingAwait = Column(Float)
    ratingAwaitCount = Column(Integer)
    ratingRfCritics = Column(Float)
    ratingRfCriticsVoteCount = Column(Integer)
    webUrl = Column(String)
    year = Column(Integer)
    filmLength = Column(Integer)
    slogan = Column(String)
    description = Column(String)
    shortDescription = Column(String)
    editorAnnotation = Column(String)
    isTicketsAvailable = Column(Boolean)
    productionStatus = Column(String)
    type = Column(String)
    ratingMpaa = Column(String)
    ratingAgeLimits = Column(String)
    hasImax = Column(Boolean)
    has3D = Column(Boolean)
    lastSync = Column(String)
    countries = Column(ARRAY(JSON))
    genres = Column(ARRAY(JSON))
    startYear = Column(Integer)
    endYear = Column(Integer)
    serial = Column(Boolean)
    shortFilm = Column(Boolean)
    completed = Column(Boolean)
    favorited_by = relationship(
        'Favorite', back_populates='movie', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Movie(id={self.id}, kinopoiskId={self.kinopoiskId}, nameOriginal={self.nameOriginal})>"
