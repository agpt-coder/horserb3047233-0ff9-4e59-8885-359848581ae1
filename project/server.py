import logging
from contextlib import asynccontextmanager
from typing import List

import project.fetch_external_api_data_service
import project.flag_explanation_for_review_service
import project.get_comic_explanation_service
import project.get_random_comic_service
import project.get_user_preferences_service
import project.review_explanation_service
import project.set_language_preference_service
import project.update_user_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="horser",
    lifespan=lifespan,
    description="Based on the details provided in our conversation and the research conducted, the final product is a web application designed to fetch and display a random xkcd comic every time it is called. The application utilizes GPT-4-vision to provide detailed explanations of the comics, which often delve into complex or scientific principles that are represented in a humorous and accessible manner. Specifically, the application is built with the following technology stack:\n\n- **Programming Language**: Python, chosen for its widespread use in both web development and machine learning, making it the perfect fit for integrating the GPT-4-vision API for comic explanations.\n- **API Framework**: FastAPI, selected for its high performance and easy-to-use features for building APIs. FastAPI's asynchronous support is ideal for handling requests to the xkcd API and GPT-4-vision API efficiently.\n- **Database**: PostgreSQL, used for storing metadata about the comics and user preferences if needed. Its reliability and powerful features support complex queries efficiently.\n- **ORM**: Prisma, to facilitate easy and secure interactions with the database using Python. Prisma provides type-safe database access, simplifying data manipulation and queries.\n\nThe application flow is as follows:\n1. The user accesses the web application.\n2. The application calls the xkcd API to fetch a random comic by generating a random number within the range of available comics and using the specific URL 'https://xkcd.com/[random_number]/info.0.json'.\n3. The comic, along with its image URL, title, and number, is displayed to the user.\n4. To provide an explanation, the application sends the comic's image URL to the GPT-4-vision API, along with a prompt to generate a detailed explanation of the comic.\n5. The GPT-4-vision API processes the image and returns a comprehensive explanation, which is then displayed to the user beneath the comic.\n\nThis tool addresses the user's requirements for a simple, intuitive interface that is accessible cloud-based for scalability and ease of access. It also meets the need for detailed explanations of xkcd comics, enhancing the appreciation and understanding of each piece.",
)


@app.get(
    "/comic/random", response_model=project.get_random_comic_service.RandomComicResponse
)
async def api_get_get_random_comic() -> project.get_random_comic_service.RandomComicResponse | Response:
    """
    Endpoint for fetching a random comic from xkcd and displaying its information.
    """
    try:
        res = await project.get_random_comic_service.get_random_comic()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/moderation/flag/{explanationId}",
    response_model=project.flag_explanation_for_review_service.FlagExplanationForReviewResponse,
)
async def api_post_flag_explanation_for_review(
    explanationId: str,
) -> project.flag_explanation_for_review_service.FlagExplanationForReviewResponse | Response:
    """
    Submit an explanation for manual review.
    """
    try:
        res = await project.flag_explanation_for_review_service.flag_explanation_for_review(
            explanationId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/preferences",
    response_model=project.update_user_preferences_service.UpdateUserPreferencesResponse,
)
async def api_put_update_user_preferences(
    userId: str, language: str, favorite_comics: List[str]
) -> project.update_user_preferences_service.UpdateUserPreferencesResponse | Response:
    """
    Endpoint to update user preferences.
    """
    try:
        res = await project.update_user_preferences_service.update_user_preferences(
            userId, language, favorite_comics
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/moderation/review/{explanationId}",
    response_model=project.review_explanation_service.ReviewExplanationResponse,
)
async def api_put_review_explanation(
    explanationId: str, approvalStatus: bool, reviewComment: str
) -> project.review_explanation_service.ReviewExplanationResponse | Response:
    """
    Endpoint for moderators to review and approve or reject explanations.
    """
    try:
        res = await project.review_explanation_service.review_explanation(
            explanationId, approvalStatus, reviewComment
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/preferences",
    response_model=project.get_user_preferences_service.UserPreferencesResponse,
)
async def api_get_get_user_preferences(
    user_id: str,
) -> project.get_user_preferences_service.UserPreferencesResponse | Response:
    """
    Endpoint to retrieve the current user preferences.
    """
    try:
        res = await project.get_user_preferences_service.get_user_preferences(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/explanation/{comicId}",
    response_model=project.get_comic_explanation_service.GetComicExplanationResponseModel,
)
async def api_get_get_comic_explanation(
    comicId: str,
) -> project.get_comic_explanation_service.GetComicExplanationResponseModel | Response:
    """
    Endpoint to retrieve a generated explanation for a specific comic.
    """
    try:
        res = await project.get_comic_explanation_service.get_comic_explanation(comicId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/i18n/language",
    response_model=project.set_language_preference_service.SetLanguagePreferenceResponse,
)
async def api_put_set_language_preference(
    user_id: str, language: str
) -> project.set_language_preference_service.SetLanguagePreferenceResponse | Response:
    """
    Endpoint for users to update their language preference.
    """
    try:
        res = await project.set_language_preference_service.set_language_preference(
            user_id, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/external/{serviceName}/{action}",
    response_model=project.fetch_external_api_data_service.FetchExternalAPIDataResponse,
)
async def api_get_fetch_external_api_data(
    serviceName: str, action: str
) -> project.fetch_external_api_data_service.FetchExternalAPIDataResponse | Response:
    """
    Generalized endpoint for fetching data from the xkcd API or GPT-4-vision with caching.
    """
    try:
        res = await project.fetch_external_api_data_service.fetch_external_api_data(
            serviceName, action
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
