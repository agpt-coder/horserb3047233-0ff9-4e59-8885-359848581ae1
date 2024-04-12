import prisma
import prisma.models
from pydantic import BaseModel


class ReviewExplanationResponse(BaseModel):
    """
    Acknowledges the review action taken by the moderator, including an update on the explanation status.
    """

    explanationId: str
    reviewStatus: bool
    message: str


async def review_explanation(
    explanationId: str, approvalStatus: bool, reviewComment: str
) -> ReviewExplanationResponse:
    """
    Endpoint for moderators to review and approve or reject explanations.

    Args:
    explanationId (str): Unique identifier of the explanation to be reviewed.
    approvalStatus (bool): Moderator's decision on the explanation - either approve or reject.
    reviewComment (str): Optional comment from the moderator providing context or rationale for their decision.

    Returns:
    ReviewExplanationResponse: Acknowledges the review action taken by the moderator, including an update on the explanation status.
    """
    explanation = await prisma.models.Explanation.prisma().update(
        where={"id": explanationId},
        data={"approvalStatus": approvalStatus, "reviewComment": reviewComment},
    )
    if explanation:
        message = "Approval" if approvalStatus else "Rejection"
        return ReviewExplanationResponse(
            explanationId=explanation.id,
            reviewStatus=True,
            message=f"Explanation {message} Successful.",
        )
    else:
        return ReviewExplanationResponse(
            explanationId=explanationId,
            reviewStatus=False,
            message="Error: Explanation Not Found or Could Not be Updated.",
        )
