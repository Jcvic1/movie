# Movie API
Movie is an API written in python using fastAPI. It performs crud operations retrieving users, authenticating with JWT, storing and retrieving user favourite movies. Movie data is extracted from kinopoiskapiuniofficial.

## Usage
- Without Docker
    * Create a virtual environment.
    * Install all requirements in ```requirements.txt```.
    * Create a ```.env``` in root folder if not available and set the following variables
    * ```DATABASE_URL```
    * ```SECRET_KEY```
    * ```ALGORITHM```
    * ```ACCESS_TOKEN_EXPIRE_MINUTES```
    * ```API_KEY```.
    * Example
    * ```DATABASE_URL=postgresql+asyncpg://user:password@app_db:5432/app_db```
    * ```SECRET_KEY="***************"```
    * ```ALGORITHM="HS256"```
    * ```ACCESS_TOKEN_EXPIRE_MINUTES=300```
    * ```API_KEY="********************",```
    * Note that database is postgres and async.
    * Run migrations (alembic) using
    * ```alembic revision --autogenerate -m "initial"```
    * ```alembic upgrade head```
    * Finally execute ```uvicorn app.main:app``` to start application
    * ```pytest -W ignore``` to start test.
- With Docker
    * Create a ```.env``` in root folder if not available and set the following variables
    * ```SECRET_KEY```
    * ```ALGORITHM```
    * ```ACCESS_TOKEN_EXPIRE_MINUTES```
    * ```API_KEY```.
    * Run ```docker compose up --build``` to start both test and application.
    * Run ```docker compose up --build web``` to start only application.
    * Run ```docker compose up --build test``` to start only test.

## Documentation
Detailed documentation of API can be accessed using swagger by going to ```/docs``` on respective domain.
