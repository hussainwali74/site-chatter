import os
from typing import Dict
from Db.models.yt_models import Channel, Video
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from Db import db_utils
load_dotenv()

DATABASE_URL = os.environ.get('MONGODB_URL')

DB_NAME = "yt_db"
CHANNELS_COLLECTION = "channels"

# MongoDB Client
client = AsyncIOMotorClient(DATABASE_URL)
database = client[DB_NAME]

# MongoDB Collections
channels_collection = database[CHANNELS_COLLECTION]


async def create_channelDetail(channel: Channel):    
    try:
        channel_dict = channel
        result = await channels_collection.insert_one(channel_dict)
        return result.inserted_id
    except Exception as e:
        print('exception in create_channelDetail=',e);
        print('--------------------------------------');
        

async def getChannelDetailsCount(query:Dict):
    "get count of channelDetails  query by channel_detail_status, video_detail_status"
    try:
        if len(query):
            count = await db_utils.count_records(channels_collection, query)
        else:
            count = await db_utils.count_records(channels_collection)
        return count
    except Exception as e:
        print('error in getChannelIds=', e)
        print('--------------------------------------')


async def getChannelDetails(query:Dict, max_results= None):
    "get list of channelDetails, query by channel_detail_status, video_detail_status and max"

    try:
        if max_results:
            result_cursor = channels_collection.find(query).limit(max_results)
        else:
            result_cursor = channels_collection.find(query)
        channelsDetails = await result_cursor.to_list(length=max_results)
        return channelsDetails
    except Exception as e:
        print('--------------------------------------')
        print('error in getChannelIds=', e)
        print('--------------------------------------')


async def get_channelDetail(id: str):
    """from channel table get one by id"""
    result = await channels_collection.find_one({"channelId": id})
    return result


async def create_channel(channel: Channel):
    channel_dict = channel.model_dump()
    result = await channels_collection.insert_one(channel_dict)
    return result.inserted_id


async def get_channel_by_id(channel_id: ObjectId):
    channel = await channels_collection.find_one({"_id": channel_id})
    return Channel(**channel)


async def create_video(video: Video):
    video_dict = video.model_dump()
    result = await videos_collection.insert_one(video_dict)
    return result.inserted_id


async def get_channel_by_id(vid_id: ObjectId):
    video = await videos_collection.find_one({"_id": vid_id})
    return Video(**video)


async def get_top_videos_by_channel_id(channel_id: ObjectId, limit: int = 10):
    # Use an aggregation pipeline to sort and limit the videos based on view count for a specific channel
    pipeline = [
        {"$match": {"channel_id": channel_id}},
        {"$sort": {"viewCount": -1}},
        {"$limit": limit}
    ]

    # Execute the aggregation pipeline
    cursor = videos_collection.aggregate(pipeline)

    # Convert the cursor result to a list of Video Pydantic models
    top_videos = [Video(**video) async for video in cursor]

    return top_videos
