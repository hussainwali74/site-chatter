from fastapi import APIRouter

from Db.models.todos_model import Todo
from Db.database import collection_name
from Db.schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Get request method
@router.get('/')
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos

@router.post('/')
async def post_todo(todo:Todo):
    collection_name.insert_one(dict(todo))