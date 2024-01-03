import base64
import requests
import json
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import logging

load_dotenv()

user = os.environ.get('WP_USER', 'default_user')
app_password = os.environ.get('WP_APP_PASSWORD', 'default_password')
WP_url = "https://balooger.com/wp-json/wp/v2"
auth = HTTPBasicAuth(username=user, password=app_password)
headers = {"Accept": "application/json", "Content-Type": "application/json"}
import pytz
logging.basicConfig(level=logging.INFO)

from datetime import datetime, timedelta
def post_creator(title, content, postStatus='publish', hours=1):

    # calculate the publish date
    publish_date = datetime.now() + timedelta(minutes=hours)
    # set the timezone to UTC
    publish_date = publish_date.astimezone(pytz.utc)

    payload = {
        "status": postStatus,
        "title": title,
        "content": content,
        "date": publish_date.isoformat(),
        "featured_media": 1612
    }
    print("-------------------------------------------------------------------------")
    print(f"{payload.get('date')=}")
    print("-------------------------------------------------------------------------")
    
    # rest of the function here
    if publish_date:
        # set the timezone to UTC
        publish_date = publish_date.astimezone(pytz.utc)
        payload["date"] = publish_date.isoformat()
    payload = json.dumps(payload)
    # rest of the function here
    try:
        res = requests.request("POST", WP_url+"/posts", data=payload, headers=headers, auth=auth)
        if res.status_code >= 200 and res.status_code < 300:
            logging.info('Post created successfully')
        else:
            logging.error('Error creating post: %s', res.json())
    except Exception as e:
        logging.error(f'Exception occurred{e=}', exc_info=True)
        
def media_creator(image_path):
    if not os.path.exists(image_path):
        logging.error(f'image does not exist at path: {image_path}')
        return None
    try:
        with open(image_path,'rb') as img_file:
            data = img_file.read()
            file_name = os.path.basename(image_path)
            
            headers={ 'Content-Type': 'image/jpg','Content-Disposition' : 'attachment; filename=%s'% file_name}
            
            img_upload_resp =  requests.request("POST", WP_url+"/media", data=data, headers=headers, auth=auth)
            if img_upload_resp.status_code >= 200 and img_upload_resp.status_code < 300:

                logging.info('media created successfully')
                resp_data = img_upload_resp.json()
                print("-------------------------------------------------------------------------")
                print(f"media {resp_data=}")
                print("-------------------------------------------------------------------------")
                
                return {"media_id": resp_data.get('id'),"media_url":resp_data.get('source_url')}
            else:
                logging.error('Error creating media: %s', img_upload_resp.json())
                return None
    except Exception as e:
        logging.error(f'Exception occurred{e=}', exc_info=True)
        return None
        
def media_details_adder(media_id, alt_text,caption, description):
    try:
        credentials = user + ':' + app_password
        token = base64.b64encode(credentials.encode())
        header_json = {'Authorization' : 'Basic ' + token.decode('utf-8')}
        # Update the uploaded image data
        update_image = {'alt_text': alt_text, 'caption': caption, 'description': description}
        updated_image_details_resp = requests.post(WP_url + '/media/' + str(media_id), headers=header_json, json=update_image)
        # updated_image_details_dict = updated_image_details_resp.json()
        if updated_image_details_resp.status_code >= 200 and updated_image_details_resp.status_code < 300:
            return 'done'
        return None
    except Exception as e:
        logging.error(f'Exception occurred{e=}', exc_info=True)

def media_creator_alt(image_path):
    WP_url = "https://balooger.com/wp-json/wp/v2"

    if not os.path.exists(image_path):
        logging.error(f'image does not exist at path: {image_path}')
        return None
    try:
        credentials = user + ':' + app_password
        token = base64.b64encode(credentials.encode())
        header_json = {'Authorization' : 'Basic ' + token.decode('utf-8')}
        media = {'file': open(image_path, "rb"), 'caption': 'My great demo picture'}
        response = requests.post(WP_url+'/media', headers=header_json, files=media)

        print("-------------------------------------------------------------------------")
        print(f"{response=}")
        print("-------------------------------------------------------------------------")
        image_json = response.json()
        # Update the uploaded image data
        update_image = {'alt_text': "my_alt_text", 'caption': "my_caption", 'description': "my_description"}
        updated_image_json = requests.post(WP_url + '/media/' + str(image_json['id']),
                                        headers=header_json, json=update_image).json()
        print("-------------------------------------------------------------------------")
        print(f"{updated_image_json=}")
        print("-------------------------------------------------------------------------")
        
        print(response.text)
    except Exception as e:
        logging.error(f'Exception occurred{e=}', exc_info=True)

def getCategories():
    try:
        res = requests.request(method='GET', url=WP_url, headers=headers, auth=auth)
        if res.status_code >= 200 and res.status_code < 300:
            logging.info('Categories fetched successfully')
        else:
            logging.error('Error fetching categories: %s', res.json())
    except Exception as e:
        logging.error(f'Exception occurred {e=}', exc_info=True)