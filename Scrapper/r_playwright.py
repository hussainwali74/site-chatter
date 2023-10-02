

import time
import random
from playwright.sync_api import sync_playwright
import re
import os
from dotenv import load_dotenv
load_dotenv()

"""
get the channel_id of channel given channel name
"""

def getChannelId(channel_name:str)->str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto('https://www.youtube.com/'+channel_name)
            # print(page.content())
            content = page.content()
            pattern = r'"https:\/\/www\.youtube\.com\/channel\/[a-zA-Z0-9_-]+"'
            match = re.search(pattern, content)
            if match:
                return match.group()
            return None
    except Exception as e:
        print('error in getting channelid',e)
        pass

def getChannelNames():
    """
    loggin to youtube and get the channel names on the first page
    """
    email =os.getenv('EMAIL')
    password =os.getenv('PASSWORD')
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch()
            page = browser.new_page()
            page.goto('https://www.youtube.com')
            # page.get_by_text('Sign in').click()
            page.get_by_label('Sign in').click()
            # page.wait_for_timeout(3000)
            email_field_selector = 'input[type="email"][name="identifier"]'
            page.wait_for_selector(email_field_selector,  state='visible')
            page.fill(email_field_selector, email)
            print('email filled')
            next_button_xpath = '//*[@id="identifierNext"]/div/button'

            # next_button_selector = 'div[id="identifierNext"] button[type="button"]'

            page.wait_for_selector(next_button_xpath,  state='visible')
            time.sleep(3)
            # page.click(next_button_xpath)
            page.keyboard.press('Enter')            
            
            password_xpath='//*[@id="password"]/div[1]/div/div[1]/input'
            password_field_selector = 'input[type="password"][name="password"]'
            page.wait_for_selector(password_xpath,  state='visible')
            page.fill(password_xpath, password)

            # password_next_btn_xpath='/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button'
            # page.click(passw)
            time.sleep(random.randint(2,4))
            page.keyboard.press('Enter')

            print('loggin complete')
            # after login,wait for page to load
            main_content_page_selector='div[id="contents"]'
            page.wait_for_selector(main_content_page_selector, state='visible')

            load_main_page_xpath='//*[@id="text"]/a'
            page.wait_for_selector(load_main_page_xpath)
            items = page.query_selector_all(load_main_page_xpath)

            # Extract the text content of each item and print it
            result = []
            for item in items:
                item_text = item.text_content()
                result.append(item_text)            
            return result
    except Exception as e:
        print('error in getting channelid',e)
        pass

print(getChannelNames())