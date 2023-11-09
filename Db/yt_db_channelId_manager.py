import os
from Db.models.yt_models import Channel, Video, ChannelId
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

from Db import db_utils
load_dotenv()

DATABASE_URL = os.environ.get('MONGODB_URL')

DB_NAME = "yt_db"
CHANNELS_ID_COLLECTION = "channel_ids"

# MongoDB Client
client = AsyncIOMotorClient(DATABASE_URL)
database = client[DB_NAME]

# MongoDB Collections
channel_ids_collection = database[CHANNELS_ID_COLLECTION]


async def createChannelId(channel_id: ChannelId):
    channel_id_dict = channel_id.model_dump()
    result = await channel_ids_collection.insert_one(channel_id_dict)
    return result.inserted_id


async def updateChannelId(channel_id: ChannelId):
    query = {'channelId': channel_id.channelId}
    update = {'$set': channel_id.model_dump()}

    result = await channel_ids_collection.update_one(query, update)
    return result.modified_count
    
async def remove_duplicates():

    # Aggregation pipeline to keep only the first occurrence of each channelId
    pipeline = [
        {"$sort": {"_id": 1}},  # Sort by _id to get the earliest documents first
        {"$group": {"_id": "$channelId", "doc_id": {"$first": "$_id"}}},
    ]

    async for doc in channel_ids_collection.aggregate(pipeline):
        # Delete all documents with the same channelId except for the first one
        result = await channel_ids_collection.delete_many({"channelId": doc["_id"], "_id": {"$ne": doc["doc_id"]}})
        print(f"Deleted {result.deleted_count} duplicates for channelId: {doc['_id']}")


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


async def getChannelIds(channel_detail_status=None, video_detail_status=None, max_results=10):
    "get list of channelIds, query by channel_detail_status, video_detail_status and max"

    try:
        query = {}
        if channel_detail_status is not None:
            query['channel_detail_status'] = channel_detail_status
        if video_detail_status is not None:
            query['video_detail_status'] = video_detail_status
        result_cursor = channel_ids_collection.find(query).limit(max_results)
        channelIds_list = await result_cursor.to_list(length=max_results)
        return channelIds_list
    except Exception as e:
        print('--------------------------------------')
        print('error in getChannelIds=', e)
        print('--------------------------------------')


async def getChannelId(id: str):
    """from channel_id table get one by id"""
    result = await channel_ids_collection.find_one({"channelId": id})
    return result
