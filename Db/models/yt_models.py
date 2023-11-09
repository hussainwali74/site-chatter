from pydantic import BaseModel
from bson import ObjectId
from typing import List


class Thumbnail(BaseModel):
    url: str
    width: int
    height: int


class ChannelId(BaseModel):
    channelId: str
    channel_detail_status: str
    video_detail_status: str


class Channel(BaseModel):
    channelId: str
    channelName: str
    channelDescription: str
    country: str
    channelPublishedAt: str
    url: str
    subscriberCount: int
    viewCount: int
    videoCount: int
    playlist_id: str
    thumbnail: Thumbnail


class Video(BaseModel):
    title: str
    videoId: str
    description: str
    thumbnail_image: Thumbnail
    channelTitle: str
    language: str
    published_date: str
    video_duration: str
    viewCount: str
    categoryId: str
    likeCount: int
    commentCount: int
    channelId: str
    tags: List[str]
