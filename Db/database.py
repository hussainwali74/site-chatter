from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri='mongodb://localhost:27017/balooger' # for local
# uri = "mongodb+srv://newuser:Exceptional7@cluster0.bjdnnbe.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

# client=MongoClient(uri)
# client.admin.command('ping')
# db=client.todo_db
# collection_name=db['todo_collections']
# collection_name.insert_one({"user_name":"Soumi"})
# s = collection_name.find()
# for i in s:

#     print('--------------------------------------');
#     print('i=',i);
#     print('--------------------------------------');

def getClient():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client
    except Exception as e:
        print('--------------------------------------');
        print('mongodb client connection error=',e);
        print('--------------------------------------');
        
