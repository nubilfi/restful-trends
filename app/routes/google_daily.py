import os
from fastapi import APIRouter, Response
from app.utils import get_cached_data_trends
from app.schemas.google_schema import GoogleResponseModel

router = APIRouter(
    prefix="/v1",
    tags=["google"],
    responses={404: {"description": "Not found"}},
)

@router.get("/google/daily_trend", response_model=GoogleResponseModel)
async def get_google_daily_trends(response: Response):
    # Define the file path
    file_path = os.path.join(os.path.dirname(__file__), '..', 'trends_data', 'google_trend_data.json')

    data = await get_cached_data_trends(file_path)

    # Set Cache-Control header for the response (30 minutes cache)
    response.headers["Cache-Control"] = "public, max-age=1800"

    return data