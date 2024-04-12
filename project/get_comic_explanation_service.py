import prisma
import prisma.models
from pydantic import BaseModel


class GetComicExplanationResponseModel(BaseModel):
    """
    Model representing the response for a request to fetch an explanation, containing the explanation text along with additional relevant information.
    """

    comicId: str
    explanation: str
    generatedBy: str
    createdAt: str


async def get_comic_explanation(comicId: str) -> GetComicExplanationResponseModel:
    """
    Endpoint to retrieve a generated explanation for a specific comic.

    Args:
    comicId (str): The unique identifier of the comic for which an explanation is being requested. This corresponds to the comic's ID in the database.

    Returns:
    GetComicExplanationResponseModel: Model representing the response for a request to fetch an explanation, containing the explanation text along with additional relevant information.
    """
    explanation_record = await prisma.models.Explanation.prisma().find_unique(
        where={"comicId": comicId}, include={"Comic": True}
    )
    if explanation_record:
        return GetComicExplanationResponseModel(
            comicId=explanation_record.comicId,
            explanation=explanation_record.text,
            generatedBy=explanation_record.generatedBy,
            createdAt=explanation_record.createdAt.isoformat(),
        )
    else:
        return GetComicExplanationResponseModel(
            comicId=comicId,
            explanation="Explanation not available.",
            generatedBy="Placeholder",
            createdAt="N/A",
        )
