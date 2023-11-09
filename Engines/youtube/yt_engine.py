from Db.models.yt_models import Channel, Video
from Tools import config
from typing import List
import random
import time
from Engines.youtube import yt_db
from googleapiclient.discovery import build, HttpError
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import os
from dotenv import load_dotenv
import asyncio
load_dotenv()


def getYoutubeClient():
    """manage api keys, return yotube client"""
    api_key = config.getYTAPIKey()

    if api_key:
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            resp = youtube.channels().list(part='snippet,contentDetails, statistics',
                                           id='UCwh0CXZfDNRGCoFdjFMvt9w').execute()
            return youtube
        except HttpError as e:
            if e.error_details[0]['reason'] == 'quotaExceeded':
                config.updateYTAPIKeyConfig(api_key)
                api_key = config.getYTAPIKey()
                if api_key:
                    return getYoutubeClient()
    return None


async def getAllChannelIdsFromYTnSave(max_ids=100, max_results_per_req=20):
    """get 2000 channel ids from ytoube and save to db"""
    async def fetch_and_save_channel_ids(next_page_token=None, total_ids=0):
        channel_ids_resp = getChannelIds(
            next_page_token=next_page_token, maxResult=max_results_per_req)
        if channel_ids_resp:

            next_page_token = channel_ids_resp.get('nextPageToken')
            channel_ids = [item['id']['channelId']
                           for item in channel_ids_resp['items']]
            await yt_db.saveChannelIds(channel_ids=channel_ids)
            total_ids += len(channel_ids_resp['items'])
            return next_page_token, total_ids
        return None, None

    total_ids = 0
    next_page_token, total_ids = await fetch_and_save_channel_ids(total_ids=total_ids)

    while next_page_token and total_ids < max_ids:
        await asyncio.sleep(random.randint(2, 8))
        print('Done saving ', total_ids, 'channel ids')
        next_page_token, total_ids = await fetch_and_save_channel_ids(
            next_page_token=next_page_token, total_ids=total_ids)
        total_ids += total_ids
    print('Done saving ', total_ids, 'channel ids')


def getChannelsStats(channel_ids: list) -> List[Channel]:
    """get Channels stats from yt API
    arguments: channel_ids, list of str channel ids"""
    youtube = getYoutubeClient()

    req = youtube.channels().list(
        part='snippet,contentDetails, statistics',
        id=','.join(channel_ids),
        maxResults=50
    )
    response = req.execute()

    datas: List[Channel] = []
    for i in range(len(response['items'])):
        item = response['items'][i]
        data: Channel = dict(
            channelId=item['id'],
            channelName=item['snippet']['title'],
            channelDescription=item['snippet']['description'],
            country=item['snippet']['country'] if 'country' in item['snippet'] else None,
            channelPublishedAt=item['snippet']['publishedAt'],
            url="https://www.youtube.com/" +
                item['snippet']['customUrl'] if 'customUrl' in item['snippet'] else None,
            subscriberCount=int(item['statistics']['subscriberCount']) if (
                item['statistics']['subscriberCount']).isdigit() else 0,
            viewCount=int(item['statistics']['viewCount']) if (
                item['statistics']['viewCount']).isdigit() else 0,
            videoCount=int(item['statistics']['videoCount']) if (
                item['statistics']['videoCount']).isdigit() else 0,
            playlist_id=item['contentDetails']['relatedPlaylists']['uploads'],
            thumbnail=item['snippet']['thumbnails'].get(
                'high'),
        )
        datas.append(data)
    return datas

# def getDataframe(datas):
#     df = pd.DataFrame(datas)
#     df['subscriberCount']=pd.to_numeric(df['subscriberCount'])
#     df['viewCount']=pd.to_numeric(df['viewCount'])
#     df['videoCount']=pd.to_numeric(df['videoCount'])
#     return df


def getDataframe(datas):
    # Check if datas is a list and not empty
    if not isinstance(datas, list) or not datas:
        raise ValueError("Input data must be a non-empty list of objects")

    # Check if all elements in datas are of the same type
    data_type = type(datas[0])
    if not all(isinstance(obj, data_type) for obj in datas):
        raise ValueError(
            "All elements in the input data must be of the same type")

    # Create DataFrame from the data
    df = pd.DataFrame(datas)

    # Convert all columns to numeric if they are not already numeric
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='ignore')

    return df


def subCountFigure(df):
    sns.set_theme(rc={'figure.figsize': (10, 5)})
    palette = sns.color_palette("rocket", len(df))
    ax = sns.barplot(x='channelName', y='subscriberCount', hue='channelName',
                     legend=False, data=df,  width=0.3, palette=palette, )

    # Format y-axis labels
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f'{x/1e6:.1f}M'))

    # Set y-axis limits
    ax.set_ylim(bottom=df['subscriberCount'].min(),
                top=df['subscriberCount'].max())

    # Display values on top of bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.savefig('figures/sub_count.png')
    # plt.show()


def viewCountFigure(df):
    sns.set_theme(rc={'figure.figsize': (10, 7)})
    palette = sns.color_palette("rocket", len(df))
    # palette = sns.color_palette("husl", len(df))

    # Define a list of colors based on a condition
    # palette = ['red' if x < 1000000 else 'green' for x in df['subscriberCount']]

    ax = sns.barplot(x='channelName', y='viewCount', hue='channelName',
                     legend=False, data=df,  width=0.3, palette=palette, )

    # Format y-axis labels
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f'{x/1e9:.2f}B'))

    # Set y-axis limits
    ax.set_ylim(bottom=df['viewCount'].min(), top=df['viewCount'].max())

    # Display values on top of bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(10, 10), textcoords='offset points')
    plt.savefig('figures/view_count.png')

    # plt.show()


def videoCountFigure(df):
    ax = sns.barplot(x='channelName', y='videoCount', data=df)
    # Display values on top of bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(10, 10), textcoords='offset points')
    plt.savefig('figures/vid_count.png')


def getChannelIds(next_page_token=None, maxResult=10):

    youtube = getYoutubeClient()

    """search channels, order by videoCount, return search response object"""
    try:
        if youtube:
            # Search for channels with 3 million or more subscribers, ordered by view count
            search_response = youtube.search().list(
                part='snippet',
                type='channel',
                order='videoCount',
                maxResults=maxResult,
                pageToken=next_page_token
            ).execute()

            if len(search_response['items']):
                # items = search_response['items']
                # next_page_token = search_response.get('nextPageToken')
                return search_response
        return []
    except HttpError as e:
        print('--------------------------------------')
        print('error  in getChannelIds=', e)


def getVideoIds(playlist_id, maxResult=10, ids_only=True):
    youtube = getYoutubeClient()
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=maxResult
    )
    response = request.execute()
    if len(response.get('items')):

        items = response['items']
        next_page_token = response.get('nextPageToken')
        more_pages = True
        if len(items) < maxResult:
            while more_pages:
                if not next_page_token:
                    more_pages = False
                else:
                    request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId=playlist_id,
                        maxResults=40,
                        pageToken=next_page_token
                    )
                    response = request.execute()
                    if len(response.get('items')):
                        items += response['items']
                        next_page_token = response.get('nextPageToken')
        if ids_only:
            return [item['contentDetails']['videoId'] for item in items]
        else:
            return items
    else:
        return []


def get_video_details(video_ids, required_fields=[]):
    """
    required_fields options:
        - Title: title of the video
        - Published_date
        - viewCount
        - likeCount
        - commentCount
    """
    try:

        youtube = getYoutubeClient()

        items = []
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(part='snippet,contentDetails,statistics',
                                            id=','.join(video_ids[i:i+50]))
            response = request.execute()
            items += response['items']
        print('--------------------------------------')
        print('len(items)=', len(items))
        print('--------------------------------------')

        video_details_dicts = []
        for i in range(len(items)):
            item = items[i]
            if item:
                thumbnail = None
                if 'thumbnails' in item['snippet']:
                    if 'maxres' in item['snippet']['thumbnails']:
                        thumbnail = item['snippet']['thumbnails'].get('maxres')
                    elif 'standard' in item['snippet']['thumbnails'] :
                        thumbnail = item['snippet']['thumbnails'].get('standard')

                d: Video = dict(
                    title=item['snippet']['title'],
                    videoId=item['id'],
                    description=item['snippet']['description'],
                    thumbnail_image=thumbnail,
                    channelTitle=item['snippet']['channelTitle'],
                    language=item['snippet']['defaultAudioLanguage'] if 'defaultAudioLanguage' in item['snippet'] else None,
                    publishedAt=item['snippet']['publishedAt'],
                    video_duration=item['contentDetails']['duration'],
                    viewCount=item['statistics']['viewCount'],
                    likeCount=item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else 0,
                    commentCount=item['statistics']['commentCount'],
                    channelId=item['snippet']['channelId'] if 'channelId' in item['snippet'] else None,
                    tags=item['snippet']['tags'] if 'tags' in item['snippet'] else None,
                )
                video_details_dicts.append(d)
        if len(required_fields):
            new_video_details_dicts = {}
            for field in required_fields:
                new_video_details_dicts[field] = [video[field] for video in video_details_dicts if field in video]
            return new_video_details_dicts
        return video_details_dicts
    except Exception as e:
        print('--------------------------------------')
        print('e=', e)
        print('--------------------------------------')
        return e


def channelVideosTop10(video_details_dicts):
    video_data_df = pd.DataFrame(video_details_dicts)
    video_data_df['Published_date'] = pd.to_datetime(
        video_data_df['Published_date']).dt.date
    video_data_df['viewCount'] = pd.to_numeric(video_data_df['viewCount'])
    video_data_df['likeCount'] = pd.to_numeric(video_data_df['likeCount'])
    video_data_df['commentCount'] = pd.to_numeric(
        video_data_df['commentCount'])
    top10_videos = video_data_df.sort_values(
        by='viewCount', ascending=False).head(10)
    return top10_videos


def videosViewsCountFigure(top10_videos):
    ax1 = sns.barplot(x='viewCount', y='Title', data=top10_videos)
    plt.savefig('figures/channel_vid_views.png')


def vidsPerMonthStatsFigure(video_details_dicts):
    video_data_df = pd.DataFrame(video_details_dicts)

    video_data_df['month'] = pd.to_datetime(
        video_data_df['Published_date']).dt.strftime('%b')
    videos_per_month = video_data_df.groupby('month', as_index=False).size()
    sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                  'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    videos_per_month.index = pd.CategoricalIndex(
        videos_per_month['month'], categories=sort_order, ordered=True)
    videos_per_month = videos_per_month.sort_index()
    sns.barplot(x='month', y='size', data=videos_per_month)
    plt.savefig('figures/vidsPerMonthStatsGraph.png')


def getChannelCompleteDetails(channel_id):
    """returns channel_details, 10 video_details"""
    channel_stats = getChannelsStats([channel_id])

    if len(channel_stats):
        playlist_id = channel_stats[0].get('playlist_id')
        video_ids = getVideoIds(playlist_id=playlist_id)
        videos_details = get_video_details(video_ids,)
        result = {}
        result['channel_details'] = channel_stats
        result['videos_details'] = videos_details
        return result
    return {'channel_details': [], 'videos_details': []}
