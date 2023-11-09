

import time
import random
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import re
import os
from dotenv import load_dotenv
load_dotenv()
channel_names_file_path='channel_names.txt'

"""
get the channel_id of channel given channel name
"""

async def getChannelIdAsync(channel_name:str, url=None)->str:
    try:
        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True, slow_mo=50)
            page = await browser.new_page()
            if url:
                await page.goto(url)
            else:
                await page.goto('https://www.youtube.com/'+channel_name)

            # Wait for the content to load (you might want to use page.wait_for_selector or other mechanisms)
            await page.wait_for_load_state("load")

            content = await page.content()
            await page.wait_for_timeout(4000)

            # print(content)
            time.sleep(random.randint(2,5))
            pattern = r'"https:\/\/www\.youtube\.com\/channel\/[a-zA-Z0-9_-]+"'
            match = re.search(pattern, content)
            if match:
                c = match.group()
                c = c.split('https://www.youtube.com/channel/')[1]
                return c
            return None
    except Exception as e:
        print('error in getting channelid',e)
        pass

def getChannelId(channel_name:str, url=None)->str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            if url:
                page.goto(url)
            else:
                page.goto('https://www.youtube.com/'+channel_name)
            # print(page.content())
            content = page.content()
            # print(content)
            time.sleep(4)
            pattern = r'"https:\/\/www\.youtube\.com\/channel\/[a-zA-Z0-9_-]+"'
            match = re.search(pattern, content)
            if match:
                return match.group()
            return None
    except Exception as e:
        print('error in getting channelid',e)
        pass

def getChannelIds():
    try:
        channel_ids=[]
        with open(channel_names_file_path, 'r') as f:
            line = f.readline()
            while line:
                # print(line.strip())
                channel_id = getChannelId(line.strip())
                if channel_id:
                    sp = channel_id.split('channel/')
                    if len(sp):
                        channel_id = sp[1]
                    print('--------------------------------------');
                    channel_id=channel_id.replace('"','')
                    print('channel_id=',channel_id);
                    print('--------------------------------------');
                    channel_ids.append(channel_id)
                line=f.readline()
        file_path='channel_ids.txt'          
        # writeToFile(file_path, channel_ids)
        with open(file_path,'w') as ff:
            for c in channel_ids:
                ff.write(c+'\n')

    except Exception as e:
        print('error in getting all channel ids: ',e)
        pass


def getChannelNames():
    """
    loggin to youtube and get the channel names on the first page
    """
    email =os.getenv('EMAIL')
    password =os.getenv('PASSWORD')
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.youtube.com')
            # -==================================================================================================
            # page.get_by_text('Sign in').click()
            # page.get_by_label('Sign in').click()
            # # page.wait_for_timeout(3000)
            # email_field_selector = 'input[type="email"][name="identifier"]'
            # page.wait_for_selector(email_field_selector,  state='visible')
            # page.fill(email_field_selector, email)
            # print('email filled')
            # next_button_xpath = '//*[@id="identifierNext"]/div/button'

            # # next_button_selector = 'div[id="identifierNext"] button[type="button"]'

            # page.wait_for_selector(next_button_xpath,  state='visible')
            # time.sleep(3)
            # # page.click(next_button_xpath)
            # page.keyboard.press('Enter')            
            
            # password_xpath='//*[@id="password"]/div[1]/div/div[1]/input'
            # password_field_selector = 'input[type="password"][name="password"]'
            # page.wait_for_selector(password_xpath,  state='visible')
            # page.fill(password_xpath, password)

            # # password_next_btn_xpath='/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button'
            # # page.click(passw)
            # time.sleep(random.randint(2,4))
            # page.keyboard.press('Enter')

            # print('loggin complete')
            # -=========================================================================================================
            # -=========================================================================================================
            #                       SEARCH INPUT 
            # -=========================================================================================================
            # password_xpath='//*[@id="password"]/div[1]/div/div[1]/input'
            search_input_xpath = 'input[type="text"][name="search_query"]'
            search_button_xpath = '//*[@id="search-icon-legacy"]'
            # search_button_xpath = 'button[id="search-icon-legacy"]'
            page.wait_for_selector(search_input_xpath,  state='visible')
            page.fill(search_input_xpath, "local data science")
            
            # password_next_btn_xpath='/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button'
            # page.click(passw)
            time.sleep(random.randint(2,4))

            page.wait_for_selector(search_button_xpath, state='visible')
            # page.locator('#search-icon-legacy').click()
            
            search_button = page.locator('#search-icon-legacy')
            print('--------------------------------------');
            print('search_button=',search_button);
            print('--------------------------------------');
            
            search_button.click()
            search_button.click()
            
            time.sleep(10)


            # -=========================================================================================================


            # ----------------------------------working
            # after login,wait for page to load
            main_content_page_selector='div[id="contents"]'
            page.wait_for_selector(main_content_page_selector, state='visible')

            details_path='div[id="details"]'
            items = page.query_selector_all(details_path)
            print(len(items))
            result = []
            for item in items:
                avatar_links = item.query_selector_all("a[id='avatar-link']")
                for link in avatar_links:
                    if '/@' in link.get_attribute('href'):
                        print(link.get_attribute('href'))
                        result.append(link.get_attribute('href'))
                    # print(link.get_attibute('href'))
         
            # ----------------------------------working
                
            # # load_main_page_xpath='//*[@id="text"]/a'
            # # time.sleep(10)
            # page.wait_for_selector(load_main_page_xpath)
            # items = page.query_selector_all(load_main_page_xpath)
            # print(items)
            # Extract the text content of each item and print it

            # for item in items:
            #     h3s=  item.query_selector_all('h3')
            #     print(len(h3s))
            #     for h3 in h3s:
            #         link = h3.query_selector_all('a')
            #         print(link[0].get_attribute('href'))

            #     # print(item.inner_html (),'\n')
            #     break
            #     item_text = item.text_content()
            #     result.append(item_text)
            # ----------------------------------working
            # existing_names = None
            # file_path='channel_names.txt'
            # if os.path.exists(file_path):
            #     with open(file_path,'r') as f:
            #         existing_names = f.read()
            # with open(file_path,'w') as f:
            #     for res in result:
            #         if res not in existing_names:
            #             f.write(res+'\n')
            # ----------------------------------working
            return result
    except Exception as e:
        print('error in getting channelid',e)
        pass

# print(getChannelId(None, "https://www.youtube.com/c/mr_indian_hacker"))
# print(getChannelNames())
# getChannelIds()