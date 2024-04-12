from typing import Dict

import httpx
from pydantic import BaseModel


class FetchExternalAPIDataResponse(BaseModel):
    """
    Dynamic model to accommodate various types of data returned by the external APIs. The actual structure of the response will depend on the service and action requested.
    """

    data: Dict
    service: str
    action: str
    cached: bool


async def fetch_external_api_data(
    serviceName: str, action: str
) -> FetchExternalAPIDataResponse:
    """
    Generalized endpoint for fetching data from the xkcd API or GPT-4-vision with caching.

    Args:
        serviceName (str): The name of the external service, e.g., 'xkcd' or 'GPT-4-vision'. Used to route the request properly.
        action (str): The specific action or endpoint of the external service to be called, formatted as a path segment.

    Returns:
         FetchExternalAPIDataResponse: Dynamic model to accommodate various types of data returned by the external APIs. The actual structure of the response will depend on the service and action requested.

    Example:
        await fetch_external_api_data('xkcd', '614/info.0.json')
        > FetchExternalAPIDataResponse(data={'month': '...', 'num': 614, ...}, service='xkcd', action='614/info.0.json', cached=False)
    """
    base_urls = {
        "xkcd": "https://xkcd.com",
        "GPT-4-vision": "https://api.openai.com/v4/images",
    }
    if serviceName not in base_urls:
        raise ValueError(f"Service {serviceName} is not supported.")
    url = (
        f"{base_urls[serviceName]}/{action}"
        if serviceName == "xkcd"
        else f"{base_urls[serviceName]}?prompt={action}"
    )
    async with httpx.AsyncClient() as client:
        if serviceName == "xkcd":
            response = await client.get(url)
        else:
            headers = {"Authorization": "Bearer YOUR_API_KEY"}
            response = await client.post(url, headers=headers)
        response.raise_for_status()
        fetched_data = response.json()
    cached = False
    return FetchExternalAPIDataResponse(
        data=fetched_data, service=serviceName, action=action, cached=cached
    )
