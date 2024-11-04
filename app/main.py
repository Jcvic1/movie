from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, movie, profile, root

app = FastAPI()

app.title = 'Movie FastAPI'
app.description = 'Light Weight API For Storing Favourite Movie Data'


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, tags=['auth'])
app.include_router(profile.router, tags=['profile'])
app.include_router(movie.router, tags=['movie'])
app.include_router(root.router, tags=['health'])
