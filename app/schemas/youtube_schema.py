from pydantic import BaseModel
from typing import List

class YoutubeContentItemBase(BaseModel):
    thumbnails_url: str
    title_text: str
    video_url: str

class YoutubeTabItemBase(BaseModel):
    tabTitle: str
    isTabActive: bool
    content: List[YoutubeContentItemBase]

class YoutubeResponseModel(BaseModel):
    results: List[YoutubeTabItemBase]
    generated_time: str
