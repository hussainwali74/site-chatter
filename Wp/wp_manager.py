import requests
import json
import random
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
load_dotenv()

user=os.environ.get('WP_USER')
app_password=os.environ.get('WP_APP_PASSWORD')

def post_creator(title, content, postStatus='publish'):
    """publish a post
    # args: 
        title = post title
        content = post content
        postStatus = publish by default for immediate publication

    """
    WP_url = "https://balooger.com/wp-json/wp/v2/posts"
    auth = HTTPBasicAuth(username=user, password=app_password)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = json.dumps({ "status":postStatus,"title": title, "content": content, "featured_media": 1612})
    try:
        res = requests.request("POST", WP_url, data=payload, headers=headers, auth=auth)
        print('--------------------------------------');
        print('res=',res.json());
        print('res=',res.status_code==201);
        print('--------------------------------------');
        
        print('done')
    except Exception as e:
        print('error publishing article: ', e)

def getCategories():
    """get the categories on the site"""
    WP_url = "https://balooger.com/wp-json/wp/v2/categories"

    auth = HTTPBasicAuth(username=user, password=app_password)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    try:
        res = requests.request(method='GET', url=WP_url, headers=headers, auth=auth)
        print('--------------------------------------');
        print('res=',res.json());
        print('res=',res.status_code==201);
        print('--------------------------------------');
        
        print('done')
    except Exception as e:
        print('error publishing article: ', e)

# post_creator("la", "en", "publish")