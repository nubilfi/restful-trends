from pydantic import BaseModel

class PingResponseModel(BaseModel):
    success: bool = True
