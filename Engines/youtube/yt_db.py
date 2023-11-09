"""
save channel details 
channel name, url,playlist_id, category, vid_count
"""

from Db.database import *
from Db.models import yt_models
from Db.models.yt_models import ChannelId
from Db.yt_db_manager import create_channelId, get_channelId, getChannelIds, getChannelIdsCount
from Db import yt_db_channelId_manager
client = getClient()


async def saveChannelIds(channel_ids: list[str]):
    saved = 0
    for id in channel_ids:
        existing_channel_id = await get_channelId(id)
        if existing_channel_id is None:
            channelId = yt_models.ChannelId(
                channelId=id, channel_detail_status='None', video_detail_status='None')
            # Insert a channel
            inserted_channel_id = await create_channelId(yt_models.ChannelId(**channelId.model_dump()))
            saved += 1
            print('inserted_channel_id=', inserted_channel_id)
            print('--------------------------------------')
    print('done saving ', saved, 'channel_ids in db')

async def updateChannelId(channel_id:ChannelId):
    try:
        await yt_db_channelId_manager.updateChannelId(channel_id,)
    except Exception as e:
        print('exception in updatechannelId=',e);
        print('--------------------------------------');
        
async def getChannelIdsForChannelDetails(max_result=10):
    channleIds = await getChannelIds(channel_detail_status='None', video_detail_status=None, max_results=max_result)
    return channleIds


async def getChannelIdsForVideoDetails(max_result=10):
    channleIds = await getChannelIds(channel_detail_status=None, video_detail_status='None', max_results=max_result)
    return channleIds


async def getAllChannelIdsCount():
    channleIds = await getChannelIdsCount(channel_detail_status=None, video_detail_status=None)
    return channleIds


async def getChannelIdsCountForChannel():
    channleIds = await getChannelIdsCount(channel_detail_status='None', video_detail_status=None)
    return channleIds


async def getChannelIdsCountForVideo():
    channleIds = await getChannelIdsCount(channel_detail_status=None, video_detail_status='None')
    return channleIds
