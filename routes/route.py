import logging
from Engines.Writer import prompts
from Wp import wp_manager
from Engines.OpenAILM import function_definitions, gpt
from Engines.Writer import blog_writer
from fastapi import APIRouter, HTTPException

from Db.models.todos_model import Todo
# from Db.database import collection_name
from Db.schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get request method
@router.get('/')
async def get_todos():
    try:
        # todos = list_serial(collection_name.find())
        logger.info("Initializing GPT LLM")
        gpt_llm = gpt.GPTLLm()
        gpt_llm.add_message('system', prompts.chat_system_prompt)

        data = {
            "channel_details": [{
                "channelName": "MrBeast",
                "url": "https://www.youtube.com/@mrbeast",
                "subscriberCount": "207000000",
                "viewCount": "36332259733",
                "videoCount": "765",
                "playlist_id": "UUX6OQ3DkcsbYNE6H8uQQuVA"
            }],
            "videos_details": {
                "Title": [
                    "I Built 100 Wells In Africa",
                    "Furthest Away From Me Wins $10,000",
                    "World's Most Expensive Bed",
                    "World's Deadliest Laser Maze!",
                    "World's Most Expensive Coffee",
                    "$100,000,000 Bathroom",
                    "$1 vs $100,000,000 House!",
                    "I Tipped A Pizza Delivery Driver A Car",
                    "World's Most Dangerous Trap!",
                    "I NEED 1 MORE SUBSCRIBER"
                ],
                "commentCount": [
                    "120677", "10310", "9876", "81199", "15781", "10712",
                    "129994", "15101", "151463", "54668"
                ]
            }
        }

        logger.info("Getting blog content")
        resp = blog_writer.getBlogContent(data)
        gpt_llm.add_message('user', resp)

        logger.info("Requesting chat completion")
        response = await gpt_llm.chat_completion_request(gpt_llm.conversation_history, function_definitions.functions)
        full_msg = response.json()['choices'][0]

        def call_functions(full_msg):
            arguments = eval(full_msg['message']['function_call']['arguments'])
            if full_msg['message']['function_call']['name'] == "post_creator":
                try:
                    logger.info("Calling post_creator function")
                    result = wp_manager.post_creator(**arguments)
                    logger.info(f"post_creator result: {result}")
                except Exception as e:
                    logger.error(f'Error in function call: {e}')
                    raise HTTPException(status_code=500, detail=f"Error in function call: {str(e)}")

        if full_msg['finish_reason'] == 'function_call':
            function_name = full_msg['message']['function_call']['name']
            logger.info(f"Calling function: {function_name}")
            call_functions(full_msg)

        logger.info("Process completed successfully")
        return {"status": "done"}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @router.post('/')
# async def post_todo(todo: Todo):
#     collection_name.insert_one(dict(todo))