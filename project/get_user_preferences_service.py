from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UserPreferencesResponse(BaseModel):
    """
    Response model representing the user's saved preferences, including language settings and favorite comics.
    """

    language: str
    favorite_comics: List[str]


async def get_user_preferences(user_id: str) -> UserPreferencesResponse:
    """
    Endpoint to retrieve the current user preferences.

    Args:
    user_id (str): ID of the user whose preferences are being retrieved. This field is assumed to be populated automatically from the user's authentication token rather than being explicitly supplied by the requester.

    Returns:
    UserPreferencesResponse: Response model representing the user's saved preferences, including language settings and favorite comics.
    """
    preferences = await prisma.models.Preferences.prisma().find_unique(
        where={"userId": user_id}
    )
    comic_views = await prisma.models.ComicView.prisma().find_many(
        where={"userId": user_id}
    )
    favorite_comics = (
        [comic_view.Comic.id for comic_view in comic_views] if comic_views else []
    )
    language = preferences.language if preferences else "en"
    response = UserPreferencesResponse(
        language=language, favorite_comics=favorite_comics
    )
    return response
