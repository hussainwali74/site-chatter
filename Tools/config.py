import json

yt_api_keys_config_file_path='Tools/yt_api_keys.json'

def getYTAPIKey():
    try:
        with open(yt_api_keys_config_file_path, 'r') as f:
            keys = json.load(f)
            for key in keys:
                if key['status'] ==1:
                    return key['key']
        return None
    except FileNotFoundError:
        print("Error: yt_api_keys.json not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in yt_api_keys.json.")
        return None
    
def updateYTAPIKeyConfig(key):
       with open(yt_api_keys_config_file_path, 'r') as f:
            keys = json.load(f)
            for k in keys:
                if k['key']==key:
                    k['status']=0
            with open(yt_api_keys_config_file_path,'w') as wf:
                json.dump(keys,wf,indent=2)
