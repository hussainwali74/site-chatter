import os
from Db.models.yt_models import Channel, Video
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from Db import db_utils
load_dotenv()

DATABASE_URL = os.environ.get('MONGODB_URL')

DB_NAME = "yt_db"
CHANNELS_ID_COLLECTION = "video_ids"

# MongoDB Client
client = AsyncIOMotorClient(DATABASE_URL)
database = client[DB_NAME]

# MongoDB Collections
video_ids_collection = database[CHANNELS_ID_COLLECTION]


async def createVideo(video: Video):
    # video_id_dict = video.model_dump()
    existing_video = await video_ids_collection.find_one({'videoId':video['videoId']})

    if not existing_video:
        result = await video_ids_collection.insert_one(video)
        return result.inserted_id

async def updateVideo(video_id: Video):
    video_id_dict = video_id.model_dump()
    result = await video_ids_collection.insert_one(video_id_dict)
    return result.inserted_id


async def getVideosCount(channel_detail_status=None, video_detail_status=None):
    "get count of Videos  query by channel_detail_status, video_detail_status"
    try:
        query = {}
        if channel_detail_status is not None:
            query['channel_detail_status'] = channel_detail_status
        if video_detail_status is not None:
            query['video_detail_status'] = video_detail_status
        if len(query):
            count = await db_utils.count_records(video_ids_collection, query)
        else:
            count = await db_utils.count_records(video_ids_collection)
        print('--------------------------------------')
        print('count=', count)
        print('--------------------------------------')
        return count
    except Exception as e:
        print('--------------------------------------')
        print('error in getVideos=', e)
        print('--------------------------------------')


async def getVideos(channel_detail_status=None, video_detail_status=None, max_results=10):
    "get list of Videos, query by channel_detail_status, video_detail_status and max"

    try:
        query = {}
        if channel_detail_status is not None:
            query['channel_detail_status'] = channel_detail_status
        if video_detail_status is not None:
            query['video_detail_status'] = video_detail_status
        result_cursor = video_ids_collection.find(query).limit(max_results)
        Videos_list = await result_cursor.to_list(length=max_results)
        return Videos_list
    except Exception as e:
        print('--------------------------------------')
        print('error in getVideos=', e)
        print('--------------------------------------')


async def getVideo(id: str):
    """from video_id table get one by id"""
    result = await video_ids_collection.find_one({"Video": id})
    return result
