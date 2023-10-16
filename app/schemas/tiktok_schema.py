from pydantic import BaseModel
from typing import List, Union

class TikTokBase(BaseModel):
    content_id: str

class TikTokFeedBase(TikTokBase):
    feed_desc: str
    feed_author_region: str
    feed_author_nickname: str
    feed_author_avatar_url: str
    feed_music_id: int
    feed_music_desc: str
    feed_music_author: str
    feed_music_url: str
    feed_author_music_url: str
    feed_video_url: str
    feed_video_views_count: str
    feed_keywords: str

class TikTokDiscoverBase(TikTokBase):
    discover_list_title: str
    discover_list_subtitle: str
    discover_list_description: str
    discover_list_url: str

class TikTokLiveBase(TikTokBase):
    live_user_id: str
    live_user_nickname: str
    live_user_country: str
    live_user_views_count: int

class TikTokResponseModel(BaseModel):
    results: List[Union[TikTokFeedBase, TikTokDiscoverBase, TikTokLiveBase]]
    generated_time: str