# videos details, channel_details -> gpt -> classify -> category, subcategory

from Engines.youtube.engine import *

def categorize_channel(channel_ids):
    channes_stats = getChannelsStats(channel_ids)
    channel_df = getDataframe(channes_stats)
    channel_video_ids = getVideoIds(channel_df)