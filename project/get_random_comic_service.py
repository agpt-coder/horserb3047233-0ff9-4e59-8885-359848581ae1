import random
from datetime import datetime

import httpx
from pydantic import BaseModel


class RandomComicResponse(BaseModel):
    """
    Response model containing the information of the randomly selected xkcd comic.
    """

    title: str
    img_url: str
    num: int
    alt_text: str
    date: str


async def get_current_comic_number() -> int:
    """
    Fetches the most recent comic from xkcd and returns its number.

    Returns:
        int: The number of the most recent xkcd comic.
    """
    url = "https://xkcd.com/info.0.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()["num"]


async def get_random_comic() -> RandomComicResponse:
    """
    Endpoint for fetching a random comic from xkcd and displaying its information.

    Returns:
        RandomComicResponse: Response model containing the information of the randomly selected xkcd comic.
    """
    current_comic_number = await get_current_comic_number()
    random_comic_number = random.randint(1, current_comic_number)
    comic_url = f"https://xkcd.com/{random_comic_number}/info.0.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(comic_url)
        response.raise_for_status()
        comic_data = response.json()
        comic_response = RandomComicResponse(
            title=comic_data["title"],
            img_url=comic_data["img"],
            num=comic_data["num"],
            alt_text=comic_data["alt"],
            date=datetime(
                year=int(comic_data["year"]),
                month=int(comic_data["month"]),
                day=int(comic_data["day"]),
            ).strftime("%Y-%m-%d"),
        )
        return comic_response
