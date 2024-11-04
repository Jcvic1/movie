from httpx import AsyncClient

from app.core.config import API_KEY
from app.utils.helper import kinopoisk_error


class KINOPOISK:
    def __init__(
        self,
    ):
        self.headers = {
            'Accept': 'application/json',
            'X-API-KEY': API_KEY,
        }
        self.base_url = 'https://kinopoiskapiunofficial.tech'

    async def search(self, query: str, page: int) -> dict:

        """search movie"""

        query = query.replace(' ', '+')

        url = f"{self.base_url}/api/v2.1/films/search-by-keyword?keyword={query}&page={page}"

        async with AsyncClient() as client:
            response = await client.get(url=url, headers=self.headers)
        if response.status_code != 200:
            await kinopoisk_error(response.status_code)
        return response.json()

    async def movie(self, id: int) -> dict:

        """retrieve movie data"""

        url = f"{self.base_url}/api/v2.2/films/{id}"

        async with AsyncClient() as client:
            response = await client.get(url=url, headers=self.headers)
        if response.status_code != 200:
            await kinopoisk_error(response.status_code)
        return response.json()
