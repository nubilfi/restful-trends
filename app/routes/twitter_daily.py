import os
from fastapi import APIRouter, Response
from app.utils import get_cached_data_trends

router = APIRouter(
    prefix="/v1",
    tags=["twitter"],
    responses={404: {"description": "Not found"}},
)

@router.get("/twitter/daily_trend")
async def get_twitter_daily_trends(response: Response, deprecated=True):
    """
    Unfortunately, Twitter Trend is not available yet.

    More info: https://developer.twitter.com/en/docs/twitter-api/migrate/twitter-api-endpoint-map
    """
    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '..', 'trends_data', 'twitter_trend_data.json')

    data = await get_cached_data_trends(file_path)

    # Set Cache-Control header for the response (30 minutes cache)
    response.headers["Cache-Control"] = "public, max-age=1800"

    return data