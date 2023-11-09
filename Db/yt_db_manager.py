import os
from Db.models.yt_models import Channel, Video, ChannelId
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from Db import db_utils
load_dotenv()

DATABASE_URL = os.environ.get('MONGODB_URL')

DB_NAME = "yt_db"
CHANNELS_COLLECTION = "channels"
CHANNELS_ID_COLLECTION = "channel_ids"
VIDEOS_COLLECTION = "videos"

# MongoDB Client
client = AsyncIOMotorClient(DATABASE_URL)
database = client[DB_NAME]

# MongoDB Collections
channels_collection = database[CHANNELS_COLLECTION]
channel_ids_collection = database[CHANNELS_ID_COLLECTION]
videos_collection = database[VIDEOS_COLLECTION]


async def create_channelId(channel_id: ChannelId):
    channel_id_dict = channel_id.model_dump()
    result = await channel_ids_collection.insert_one(channel_id_dict)
    return result.inserted_id


async def getChannelIdsCount(channel_detail_status=None, video_detail_status=None):
    "get count of channelIds  query by channel_detail_status, video_detail_status"
    try:
        query = {}
        if channel_detail_status is not None:
            query['channel_detail_status'] = channel_detail_status
        if video_detail_status is not None:
            query['video_detail_status'] = video_detail_status
        if len(query):
            count = await db_utils.count_records(channel_ids_collection, query)
        else:
            count = await db_utils.count_records(channel_ids_collection)
        print('--------------------------------------')
        print('count=', count)
        print('--------------------------------------')
        return count
    except Exception as e:
        print('--------------------------------------')
        print('error in getChannelIds=', e)
        print('--------------------------------------')


async def getChannelIds(channel_detail_status=None, video_detail_status=None, max_results=None):
    "get list of channelIds, query by channel_detail_status, video_detail_status and max"

    try:
        query = {}
        if channel_detail_status is not None:
            query['channel_detail_status'] = channel_detail_status
        if video_detail_status is not None:
            query['video_detail_status'] = video_detail_status
            
        if max_results:
            result_cursor = channel_ids_collection.find(query).limit(max_results)
        else:
            result_cursor = channel_ids_collection.find(query)

        channelIds_list = await result_cursor.to_list(length=max_results)
        return channelIds_list
    except Exception as e:
        print('--------------------------------------')
        print('error in getChannelIds=', e)
        print('--------------------------------------')


async def get_channelId(id: str):
    """from channel_id table get one by id"""
    result = await channel_ids_collection.find_one({"channelId": id})
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
