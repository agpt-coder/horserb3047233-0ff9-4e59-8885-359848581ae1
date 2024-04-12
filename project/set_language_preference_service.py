import prisma
import prisma.models
from pydantic import BaseModel


class SetLanguagePreferenceResponse(BaseModel):
    """
    Confirms the successful update of the user's language preference.
    """

    success: bool
    message: str


async def set_language_preference(
    user_id: str, language: str
) -> SetLanguagePreferenceResponse:
    """
    Endpoint for users to update their language preference.

    This function checks if the user's preferences exist. If so, it updates the language preference;
    if not, it creates a new preference entry with the specified language.

    Args:
        user_id (str): The unique identifier of the user updating their language preference.
        language (str): The requested language setting to be applied for the user's interface.

    Returns:
        SetLanguagePreferenceResponse: Confirms the successful update of the user's language preference.

    Example:
        await set_language_preference("some-user-id", "en")
        > SetLanguagePreferenceResponse(success=True, message="Language preference updated successfully.")
    """
    preference = await prisma.models.Preferences.prisma().find_unique(
        where={"userId": user_id}
    )
    if preference:
        await prisma.models.Preferences.prisma().update(
            where={"userId": user_id}, data={"language": language}
        )
    else:
        await prisma.models.Preferences.prisma().create(
            data={"userId": user_id, "language": language}
        )
    return SetLanguagePreferenceResponse(
        success=True, message="Language preference updated successfully."
    )
