from typing import List

from pydantic import BaseModel


class UserPreferences(BaseModel):
    """
    Detailed user preferences including language settings and favorite comics.
    """

    language: str
    favorite_comics: List[str]


class UpdateUserPreferencesResponse(BaseModel):
    """
    Response model returned after updating user preferences indicating success and possibly returning the updated preferences.
    """

    success: bool
    message: str
    updated_preferences: UserPreferences


async def update_user_preferences(
    userId: str, language: str, favorite_comics: List[str]
) -> UpdateUserPreferencesResponse:
    """
    Endpoint to update user preferences.

    Args:
        userId (str): Unique identifier for the user whose preferences are being updated.
        language (str): Preferred user language setting.
        favorite_comics (List[str]): List of user's favorite comic IDs.

    Returns:
        UpdateUserPreferencesResponse: Response model returned after updating user preferences
        indicating success and possibly returning the updated preferences.
    """
    import prisma.models

    current_preferences = await prisma.models.Preferences.prisma().find_unique(
        where={"userId": userId}
    )
    if current_preferences:
        await prisma.models.Preferences.prisma().update(
            where={"userId": userId}, data={"language": language}
        )
        success = True
        message = "User preferences updated successfully."
    else:
        success = False
        message = "User preferences could not be found for the provided userId."
    updated_user_preferences = UserPreferences(
        language=language, favorite_comics=favorite_comics
    )
    return UpdateUserPreferencesResponse(
        success=success,
        message=message,
        updated_preferences=updated_user_preferences if success else None,
    )
