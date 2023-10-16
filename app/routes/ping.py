from fastapi import APIRouter, Response
from app.schemas.ping_schema import PingResponseModel

router = APIRouter(
    prefix="/v1",
    tags=["ping"],
    responses={404: {"description": "Not found"}},
)

@router.get("/ping", response_model=PingResponseModel)
async def ping_api(response: Response):
    """
    If this endpoint return `200`, the server is _healthy_.
    """
    response.headers["Cache-Control"] = "public, max-age=1800"
    return {"success": True}
