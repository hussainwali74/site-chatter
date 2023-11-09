"""manages channel details
   get, update channel details
"""
from typing import List
from Db.models.yt_models import Channel, ChannelId
from Db.yt_db_manager import getChannelIds
from Db.yt_db_channel_manager import create_channelDetail
from Engines.youtube import yt_engine
from Engines.youtube import yt_db

async def saveNChannelDetails(n:int):
    resp = await getChannelIds(channel_detail_status='None',max_results=n)
    
    if resp and len(resp):
        channel_ids = [id['channelId'] for id in resp]
        total_saved = 0
        channel_stats:List[Channel] = []
        if len(channel_ids)>50:
            for i in range(0,len(channel_ids), 50):
                in_channel_ids = channel_ids[i:i+50]
                
                channel_stats = yt_engine.getChannelsStats(channel_ids=in_channel_ids)

                total_saved += len(channel_stats)
        else:
            channel_stats= yt_engine.getChannelsStats(channel_ids=channel_ids)
            total_saved += len(channel_stats)

        
        for c in channel_stats:
            resp = await create_channelDetail(c)
            if resp:
                channel_id = ChannelId(channel_detail_status='done',channelId=c['channelId'],video_detail_status='None')
                await yt_db.updateChannelId(channel_id=channel_id)

        print('sAved: len(channel_stats)=',total_saved);
        print('--------------------------------------');
