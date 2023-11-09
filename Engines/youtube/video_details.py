"""manages channel details
   get, update channel details
"""
from typing import List
from Db.models.yt_models import Video, ChannelId
from Db.yt_db_manager import getChannelIds
from Db.yt_db_channel_manager import getChannelDetails
from Db.yt_db_video_manager import createVideo
from Engines.youtube import yt_engine
from Engines.youtube import yt_db

async def saveNVideoDetails(n:int, perchannel_video=10):
    """save videos of n channels, n is the number of channels
        getting channel ids -> playlist id of each channel -> videos  in the playlist (be careful many videos) 
        -> save channel details in db -> update channelId video done
    """
    try:
        #get channel ids where channeldetail status is done
        channs = await yt_db.getChannelIds(channel_detail_status='done', video_detail_status='None', max_results=n)
        channel_ids = [c['channelId'] for c in channs]

        for channel_id in channel_ids:
            # print('getting channelDetails')
            channel_details = await getChannelDetails(query={"channelId":channel_id})
        
            playlist_id = channel_details[0]['playlist_id']
            print('getting videoids')
            video_ids =  yt_engine.getVideoIds(playlist_id=playlist_id, maxResult=perchannel_video)
            # print('--------------------------------------');
            # print('video_ids=',video_ids);
            # print('--------------------------------------');

            if video_ids and len(video_ids) :
                print('getting video details', len(video_ids) )
                video_details:List[Video] = yt_engine.get_video_details(video_ids=video_ids)
                print('--------------------------------------');
                print('video_details=',len(video_details));
                print('--------------------------------------');
                
                total_saved = 0
                for video_detail in video_details:
                    print('creating video in db')
                    resp = await createVideo(video= video_detail)                
                    print('--------------------------------------');
                    print('created video id=',resp);
                    print('--------------------------------------');
                    
                    if resp:
                        channel_id_model = ChannelId(channel_detail_status='done', video_detail_status='done',channelId=channel_id)
                        print('updating channelId')
                        await yt_db.updateChannelId(channel_id=channel_id_model)
                        total_saved+=1
                print('sAved: len(videos)=',total_saved);
                print('--------------------------------------');
                
    except Exception as e:
        print('--------------------------------------');
        print('exception in saveNVideoDetails=',e);
        print('--------------------------------------');
        