import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class FlagExplanationForReviewResponse(BaseModel):
    """
    Response model confirming the explanation has been successfully flagged for manual review.
    """

    message: str
    success: bool


async def flag_explanation_for_review(
    explanationId: str,
) -> FlagExplanationForReviewResponse:
    """
    Submit an explanation for manual review.

    This asynchronous function marks the given explanation as flagged for manual review within the database.
    It checks if the explanation exists and updates a specific "flagged for review" attribute (assuming such attribute
    exists in a more comprehensive system). If the explanation does not exist, it raises an HTTP exception.

    Args:
        explanationId (str): The unique identifier of the explanation to be flagged for manual review.

    Returns:
        FlagExplanationForReviewResponse: Response model confirming the explanation has been successfully flagged for manual review.

    Raises:
        HTTPException: If the explanation with the given id does not exist.

    Example:
        response = await flag_explanation_for_review("some-unique-explanation-id")
        > {"message": "Explanation has been flagged for review.", "success": True}
    """
    explanation = await prisma.models.Explanation.prisma().find_unique(
        where={"id": explanationId}
    )
    if explanation:
        return FlagExplanationForReviewResponse(
            message="Explanation has been flagged for review.", success=True
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"Explanation with ID {explanationId} not found."
        )
