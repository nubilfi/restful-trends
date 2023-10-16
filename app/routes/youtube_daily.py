import os
import json
from fastapi import APIRouter, Response
from app.utils import get_cached_data_trends
from app.schemas.youtube_schema import YoutubeResponseModel

router = APIRouter(
    prefix="/v1",
    tags=["youtube"],
    responses={404: {"description": "Not found"}},
)

@router.get("/youtube/daily_feed", response_model=YoutubeResponseModel)
async def get_youtube_daily_feed_trends(response: Response):
    """
    We use web scraping to collect YouTube Trends, the output is already adjusted to have `tabbed` section.
    """
    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '..', 'trends_data', f"youtube_trend_data.json")

    data = await get_cached_data_trends(file_path)

   # Set Cache-Control header for the response (30 minutes cache)
    response.headers["Cache-Control"] = "public, max-age=1800"

    return data

