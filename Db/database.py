from pymongo import MongoClient
uri='mongodb://localhost:27017/test' # for local
uri = "mongodb+srv://admin:test1234@cluster0.bjdnnbe.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
client=MongoClient(uri)

db=client.todo_db
collection_name=db['todo_collection']