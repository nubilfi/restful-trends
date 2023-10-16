from pydantic import BaseModel
from typing import List

class GoogleResponseModel(BaseModel):
    results: List[str]
    generated_time: str
