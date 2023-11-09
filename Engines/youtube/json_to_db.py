"""
take the channel channel info from data/json
get channel id using playwright, 
get channel details using yt api
clean data and save to db
"""
from Scrapper import r_playwright
import ijson
import time
import random
async def getJsonFileData(file_path):
    ids= []
    with open(file_path, 'r', encoding='utf-8') as f:
        categories_n_data = ijson.items(f,'item') 
        i = 1
        for item in categories_n_data:
            category = item['category']
            data = item['data']
            for d in data:
                d['category'] = category
                if '/youtube/c/' in d['link']:
                    d['link'] = d['link'].replace('/youtube/c/', 'https://www.youtube.com/c/')
                else:
                    d['link'] = d['link'].replace('/youtube/channel/', 'https://www.youtube.com/channel/')
    
            for d in data:
                print(i, d['link'], '\n')
                if 'youtube.com/channel' in d['link']:
                    id = d['link'].split('channel/')[1]
                elif 'youtube.com/c/' in d['link']:
                    id = await r_playwright.getChannelIdAsync(None, url=d['link'])
                else: 
                    id = None

                print('--------------------------------------');
                print('id=',id);
                print('--------------------------------------');
                if id:
                    ids.append(id)
                    time.sleep(random.randint(3,6))
                i+=1
            break
    return ids