import os
from fastapi import APIRouter, Response
from app.utils import get_cached_data_trends
from app.schemas.tiktok_schema import TikTokResponseModel

router = APIRouter(
    prefix="/v1",
    tags=["tiktok"],
    responses={404: {"description": "Not found"}},
)

@router.get("/tiktok/daily_feed/{type}", response_model=TikTokResponseModel)
async def get_tiktok_daily_feed_trends(response: Response, type: str):
    """
    There are 3 types of data available: `feed`, `discover` and `live_channels`.
    """
    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '..', 'trends_data', f"tiktok_{type}_data.json")

    data = await get_cached_data_trends(file_path)

    # Set Cache-Control header for the response (30 minutes cache)
    response.headers["Cache-Control"] = "public, max-age=1800"

    return data
