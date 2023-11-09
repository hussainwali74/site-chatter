# """
# save channel details
# channel name, url,playlist_id, category, vid_count
# """
# import markdown
# from Db.database import *
# client = getClient()
# from Engines.youtube import json_to_db

# -------------------------------------------------------------------------------------------------------- channel details
# from Engines.youtube import yt_engine
# x = yt_engine.getChannelCompleteDetails('UCbCmjCuTUZos6Inko4u57UQ')
# print('--------------------------------------');
# print('x=',x);
# print('--------------------------------------');
# --------------------------------------------------------------------------------------------------------
# from motor.motor_asyncio import AsyncIOMotorClient
# client = AsyncIOMotorClient("<MongoDB connection string>")
# db = client["library"]

# x ={"MrBeast": {'channel_details': [{'channelName': 'MrBeast', 'url': 'https://www.youtube.com/@mrbeast', 'subscriberCount': '207000000', 'viewCount': '36332259733', 'videoCount': '765', 'playlist_id': 'UUX6OQ3DkcsbYNE6H8uQQuVA'}], 'videos_details': {'Title': ['I Built 100 Wells In Africa', 'Furthest Away From Me Wins $10,000', 'World’s Most Expensive Bed', 'World’s Deadliest Laser Maze!', 'World’s Most Expensive Coffee', '$100,000,000 Bathroom', '$1 vs $100,000,000 House!', 'I Tipped A Pizza Delivery Driver A Car', "World's Most Dangerous Trap!", 'I NEED 1 MORE SUBSCRIBER'], 'commentCount': ['120677', '10310', '9876', '81199', '15781', '10712', '129994', '15101', '151463', '54668']}}}
# import pymongo
# from Db import database

# Connect to the MongoDB server
# client = database.getClient()

# # Access the database
# dbname = client['yt_library']
# collection_name = dbname['channel_details']

# Insert the document into the collection
# collection_name.insert_one(x)

# -------------------------------------------------------------------------------------------------------------db test
# import asyncio

# from Db.yt_db_manager import *
# async def main():
#     # Assuming you have a Channel instance to insert
#     channel_data = {
#         "channelId": "TestChannel",
#         "channelName": "Test Channel",
#         "channelDescription": "Description",
#         "country": "US",
#         "channelPublishedAt": "2023-01-01",
#         "url": "https://example.com",
#         "subscriberCount": 1000,
#         "viewCount": 50000,
#         "videoCount": 100,
#         "playlist_id": "test_playlist",
#         "thumbnail": {
#             "url": "https://example.com/image.jpg",
#             "width": 100,
#             "height": 100
#         }
#     }

#     # Insert a channel
#     inserted_channel_id = await create_channel(Channel(**channel_data))
#     print(f"Inserted Channel ID: {inserted_channel_id}")

#     # Retrieve the inserted channel by ID
#     retrieved_channel = await get_channel_by_id(inserted_channel_id)
#     print("Retrieved Channel:")
#     print(retrieved_channel.model_dump_json())

# if __name__ == "__main__":
#     asyncio.run(main())

# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------db test
from googleapiclient.discovery import build
import asyncio

from Db.yt_db_manager import *
from Engines.youtube import yt_engine
from Engines.youtube import yt_db
import time
import random

from Engines.youtube.channel_details import saveNChannelDetails
from Engines.youtube.video_details import saveNVideoDetails

from Db.yt_db_channelId_manager import remove_duplicates
async def main():

    # await yt_engine.getAllChannelIdsFromYTnSave(max_ids=30,max_results_per_req=10) # working done

    # x = await yt_db.getChannelIds() #works, get all channelids
    
    # vidChannelIds = await yt_db.getAllChannelIdsCount() # working done
    # print('--------------------------------------');
    # print('vidChannelIds=',vidChannelIds);
    # print('--------------------------------------');
    
    
    # take n channelids and get their details and save to db

    #this will be called from yt_engine
    # await remove_duplicates() # works
    # resp = await saveNChannelDetails(220) # WORKS

    resp = await saveNVideoDetails(1) # WORKS


    # print('--------------------------------------');
    # print('resp=',resp);
    # print('--------------------------------------');
    
    # channel_ids= ['UCNye-wNBqNL5ZzHSJj3l8Bg', 'UCNye-wNBqNL5ZzHSJj3l8Bg', 'UCYlh4lH762HvHt6mmiecyWQ', 'UCNye-wNBqNL5ZzHSJj3l8Bg', 'UCYlh4lH762HvHt6mmiecyWQ', 'UCNye-wNBqNL5ZzHSJj3l8Bg', 'UCYlh4lH762HvHt6mmiecyWQ', 'UCNye-wNBqNL5ZzHSJj3l8Bg', 'UCYlh4lH762HvHt6mmiecyWQ', 'UCNye-wNBqNL5ZzHSJj3l8Bg']   
    # x = await yt_engine.getChannelsStats(channel_ids=channel_ids)
    # print('--------------------------------------');
    # print('x=',x);
    # print('--------------------------------------');
    


    # Assuming you have a Channel instance to insert
#     # ids = await json_to_db.getJsonFileData('D:/work/balooger/app/data/top100data.json')
#     # ids= ['UCwh0CXZfDNRGCoFdjFMvt9w', None, '"https://www.youtube.com/channel/UCVEvXfblll0OjxBE_I9YeOw"', 'UCQmRC_d2-ilErjEHUrzQF9A', '"https://www.youtube.com/channel/UC8m8-P5KTTN3q6Fzm4Hg-Jg"', '"https://www.youtube.com/channel/UCKygRpISlqs5TufcT3JtRng"', 'UCdytajrJerhsRluwyYyAOlQ', '"https://www.youtube.com/channel/UCFCtZJTuJhE18k8IXwmXTYQ"', 'UCtaBL35pjhdJyCbA7tECN8g', None, 'UC-5_KlNZB24vRngk6fxxKSQ', '"https://www.youtube.com/channel/UC_DmOS_FBvO4H27U7X0OtRg"', None, '"https://www.youtube.com/channel/UCFLa8WnVtm9REH0CejH45MQ"', '"https://www.youtube.com/channel/UCqOYr6Lz-AgemZXNUPjx2fQ"', '"https://www.youtube.com/channel/UCx055nOixUqvuOTWRdVJYhw"', 'UC-GOyGEDriYrFgkWDPUWEUQ', 'UC2asXnNIkyag4jZkAgadGlQ', 'UCwPzq5yQwczLmivBX8zq7Mw', '"https://www.youtube.com/channel/UC9hCQoT-VY7vVRaC62WJOJw"', '"https://www.youtube.com/channel/UCNFdrFWghNFqxgRgR6q8MJA"', '"https://www.youtube.com/channel/UC2tXSNh29alZzZJs2sznqXg"', '"https://www.youtube.com/channel/UCLWCLAx6Gbs2J75Ts5IAiKA"', 'UChLALLAEdFb5NSpAGw1WyiQ', '"https://www.youtube.com/channel/UCSK1_qvsEuTNZnvLQvNRLGQ"', 'UCf40JWoJDqUh3ZeyJ5p76tA', 'UCkmLpbIFpQS0MOJr0FOY_nw', None, 'UC0PzFex_aMkn11CnoYvYeXw', 'UCymmAHzNoB02H2G_sfvX6ag', '"https://www.youtube.com/channel/UCWhnmZWSKc4l5XPNr8wd0YA"', 'UCg4sfCrzkbjak7-p0Knv4xQ', '"https://www.youtube.com/channel/UCKH0DuBnfp2Ox7QF8ICsZHQ"', '"https://www.youtube.com/channel/UC6BX35RIJUH3tRQ3UiQkC1w"', '"https://www.youtube.com/channel/UC81vkOUQ5BoMmSC4lFzGB7g"', None, '"https://www.youtube.com/channel/UCmGSJVG3mCRXVOP4yZrU1Dw"', '"https://www.youtube.com/channel/UCZOcZonhmKbNGeSZGJpa5Aw"', '"https://www.youtube.com/channel/UCYGr30uAQvrMrdPBNlyoM2w"', 'UCnGMrsmyA2qUoR1cuHykBeA', 'UCiehVyp1HPDFFqZzOAeTLAg', 'UC8AAXDNsPVklZlCfqFtG6Bg', 'UCTuN27bHgEAN8WmAA2Zd24w', 'UCA69MS54Tv5-utw2g-N5_IA', 'UClnfG0wryFSVWcmkQ_VCFTw', 'UC3Bv5aWP1mouezKK_y9MawA', 'UCnBS7eZ5EA0seHV8gX-FXQw', 'UCRtmi8qm_EtuDhcR2eykFNQ', 'UCo8aFzFNVJPsIINsdWuIhUA', 'UCprjYvd-7fC8zPYRa8oXDrg', None, '"https://www.youtube.com/channel/UChsWRtPH1RZ2TCfHF_TP_kA"', '"https://www.youtube.com/channel/UCDMxRQIExOxssGxCMkNBMhA"', 'UCjUgDyFD84_lDeD0MsI4T-g', 'UClqc_ZRyx7vYf_zfBFXQ4Lw', 'UCympKTLm_mKQmUFrF0GB_cA', '"https://www.youtube.com/channel/UC_sOtcSKcivKayYiRjzYLeg"', 'UCciYvnRWZaLN7S_4ky-UWog', 'UCMGoq1AJiIZMVbKU7elvF8w', 'UCe6jfiVoQBMlFIIXoIVVGXA', '"https://www.youtube.com/channel/UCugqOjnkPkUX9T6GcmuTX-g"', '"https://www.youtube.com/channel/UCcAd5Np7fO8SeejB1FVKcYw"', 'UCLWZclmxxZ03pNHJwv2PcSA', '"https://www.youtube.com/channel/UCLvEK5IsuSZSErmoU1fOwog"', '"https://www.youtube.com/channel/UCDxjhss7qTdHYLMchzmRn3w"', '"https://www.youtube.com/channel/UC7vTq7aY0zIbr8a2Fa0a_Zw"', 'UCAvtlB613tt7Q0Al0b8GlmQ', 'UCUeU1MvI_rvQG5_Stnhq6LQ', None, '"https://www.youtube.com/channel/UCqUbXQr-AQWPID4K0TF3L5Q"', 'UC6wgvBEpAERL_8Ro8uR4NQg', '"https://www.youtube.com/channel/UCZxGwa7S2StnCA8k_IHFfpA"', '"https://www.youtube.com/channel/UCStzHveCf_orXJ-19kiOUog"', '"https://www.youtube.com/channel/UCeqR9E_-abAfyQ38x2Uigeg"', '"https://www.youtube.com/channel/UC7aFJl_PxpkBkrFmd-QHnLw"']
#     print('--------------------------------------')
#     # print('ids=',ids);
#     print('--------------------------------------')
#     # file_utils.writeToFile('data/all_channel_ids.txt',ids)

# # Set up the YouTube API client
    # api_key='AIzaSyCIh2k9kClt5VPZZFC2xQyy__VjgGEDdUc'
    # youtube = build('youtube', 'v3', developerKey=api_key)
    # # Search for channels with 3 million or more subscribers, ordered by view count
    # search_response = youtube.search().list(
    #     part='snippet',
    #     type='channel',
    #     order='videoCount',
    #     maxResults=1
    # ).execute()
    # print('--------------------------------------')
    # print('search_response=', search_response)
    # print('--------------------------------------')

# # Extract channel IDs from the search results
# channel_ids = [item['id']['channelId'] for item in search_response['items']]

# # Retrieve channel information including subscriber count
# channels_response = youtube.channels().list(
#     part='snippet,statistics',
#     id=','.join(channel_ids),
#     maxResults=50
# ).execute()

# # Sort the channels based on the subscriber count in descending order
# sorted_channels = sorted(channels_response['items'], key=lambda x: int(x['statistics']['subscriberCount']), reverse=True)

# # Print the sorted channels
# for channel in sorted_channels:
#     channel_title = channel['snippet']['title']
#     channel_subscriber_count = channel['statistics']['subscriberCount']
#     print(f"Channel: {channel_title}")
#     print(f"Subscriber Count: {channel_subscriber_count}")
#     print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

# -------------------------------------------------------------------------------------------------------------
# res = collection_name.find()
# for r in res:
#     print('--------------------------------------');
#     print('r=',r);
#     print('--------------------------------------');

# # # print('--------------------------------------');
# # # print('x=',x);
# # # print('len(x)=',len(x));
# # # print('--------------------------------------');
# # # from Engines.Writer import prompts
# # from Engines.Writer import blog_writer
# # # resp = blog_writer.getBlogContent(x)
# # arguments= {'title': 'MrBeast: The YouTube Channel That Gives Back to the World', 'content': "Welcome to the world of MrBeast, the YouTube channel that has captured the hearts of millions of viewers worldwide. With over 207 million subscribers and 36 billion views, MrBeast has become a household name in the YouTube community. But what sets this channel apart from the rest? In this comprehensive blog post, we will delve into the complete data of the channel and explore its niche, history, growth, and most popular videos. We will also take a closer look at the creator's journey, motivations, and future plans. So, let's dive in and discover the world of MrBeast!\n\n### Channel Basic Information\n- Channel Name: MrBeast\n- URL: [MrBeast YouTube Channel](https://www.youtube.com/@mrbeast)\n- Subscriber Count: 207 million\n- View Count: 36 billion\n- Video Count: 765\n- Playlist ID: UUX6OQ3DkcsbYNE6H8uQQuVA\n\n### Niche and Theme\nMrBeast's niche is a unique blend of entertainment, philanthropy, and challenges. The channel's theme revolves around giving back to the world while entertaining its viewers. MrBeast's videos are a perfect mix of fun, excitement, and heartwarming moments that leave a lasting impact on its audience.\n\n### Brief History of Creation\nMrBeast was created in 2012 by Jimmy Donaldson, a young entrepreneur from North Carolina, USA. Initially, the channel focused on gaming videos, but it wasn't until 2017 that MrBeast found its true calling. Jimmy started incorporating philanthropy into his videos, and that's when the channel's popularity skyrocketed. Today, MrBeast is one of the most-watched channels on YouTube, with millions of loyal fans eagerly waiting for each new video.\n\n### Type of Content\nMrBeast's content is diverse and caters to a wide range of audiences. The channel's videos can be categorized into three main types: challenges, philanthropy, and entertainment. The challenges range from simple tasks to extreme stunts, while the philanthropy videos showcase MrBeast's efforts to give back to the world. The entertainment videos feature unique and creative content that keeps viewers hooked.\n\n### Unique Aspects\nOne of the most unique aspects of MrBeast's channel is its focus on giving back to the world. Unlike other YouTube channels, MrBeast's videos have a deeper purpose and impact. The channel's philanthropic efforts have inspired millions of viewers to do good and make a positive change in the world. Another unique aspect is the channel's growth and milestones, which we will explore in the next section.\n\n### Growth and Milestones\nMrBeast's growth has been nothing short of phenomenal. In just a few years, the channel has amassed over 207 million subscribers and 36 billion views. This growth has been fueled by the channel's unique content and its creator's dedication to making a difference in the world. MrBeast has also achieved several milestones, including being the first YouTuber to plant 20 million trees and the first to give away $1 million in a single video.\n\n### Most Popular Videos\nMrBeast's most popular videos have garnered millions of views and have become viral sensations. Let's take a closer look at the top 10 most popular videos on the channel and the reasons for their success.\n1. I Built 100 Wells In Africa\n2. Furthest Away From Me Wins $10,000\n3. World's Most Expensive Bed\n4. World's Deadliest Laser Maze!\n5. World's Most Expensive Coffee\n6. $100,000,000 Bathroom\n7. $1 vs $100,000,000 House!\n8. I Tipped A Pizza Delivery Driver A Car\n9. World's Most Dangerous Trap!\n10. I NEED 1 MORE SUBSCRIBER\n\n### Engagement and Feedback\nMrBeast's videos have received overwhelming engagement and feedback from viewers. The channel's videos have an average of over 100,000 comments, with some videos receiving over 1 million comments. The impact of these videos can be seen in the thousands of heartwarming stories shared by viewers in the comments section. MrBeast's videos have also received positive feedback from viewers, with many praising the channel's unique content and philanthropic efforts.\n\n### Creator's Journey\nJimmy Donaldson's journey to becoming MrBeast has been nothing short of inspiring. From starting out as a gaming YouTuber to becoming a philanthropist and entertainer, Jimmy has come a long way. His journey has been filled with challenges and obstacles, but his determination and passion have helped him overcome them. Today, Jimmy is not only a successful YouTuber but also a role model for millions of viewers worldwide.\n\n### Motivations and Behind-the-Scenes\nJimmy's motivations for creating MrBeast's channel were simple - to entertain and make a positive impact in the world. His passion for giving back to the community and making a difference has been the driving force behind the channel's success. Behind-the-scenes, Jimmy and his team work tirelessly to create unique and engaging content that resonates with viewers. Their dedication and hard work have made MrBeast one of the most-watched channels on YouTube.\n\n### Future Plans and Collaborations\nMrBeast's future plans include continuing to create entertaining and impactful content for its viewers. The channel also has several collaborations in the works, including partnerships with other YouTubers and organizations. These collaborations will not only help MrBeast reach a wider audience but also make a bigger impact in the world.\n\n### Conclusion\nIn conclusion, MrBeast's channel has become a global phenomenon, thanks to its unique content and philanthropic efforts. With millions of loyal fans and billions of views, MrBeast has made a lasting impact on the YouTube community. The channel's growth and milestones, most popular videos, and the creator's journey and motivations have inspired millions of viewers worldwide. As MrBeast continues to entertain and give back to the world, we can't wait to see what the future holds for this incredible channel."}
# # arguments['content'] = markdown.markdown(arguments['content'])
# # from Wp import wp_manager

# # # wp_manager.post_creator(**arguments)
# # wp_manager.getCategories()
