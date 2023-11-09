from Engines.Writer import prompts
from Wp import wp_manager
from Engines.OpenAILM import function_definitions, gpt
from Engines.Writer import blog_writer
from fastapi import APIRouter

from Db.models.todos_model import Todo
# from Db.database import collection_name
from Db.schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

# Get request method
@router.get('/')
async def get_todos():
    # todos = list_serial(collection_name.find())
    gpt_llm = gpt.GPTLLm()
    gpt_llm.add_message('system',prompts.chat_system_prompt)

    x = x= {'channel_details': [{'channelName': 'MrBeast', 'url': 'https://www.youtube.com/@mrbeast', 'subscriberCount': '207000000', 'viewCount': '36332259733', 'videoCount': '765', 'playlist_id': 'UUX6OQ3DkcsbYNE6H8uQQuVA'}], 'videos_details': {'Title': ['I Built 100 Wells In Africa', 'Furthest Away From Me Wins $10,000', 'World’s Most Expensive Bed', 'World’s Deadliest Laser Maze!', 'World’s Most Expensive Coffee', '$100,000,000 Bathroom', '$1 vs $100,000,000 House!', 'I Tipped A Pizza Delivery Driver A Car', "World's Most Dangerous Trap!", 'I NEED 1 MORE SUBSCRIBER'], 'commentCount': ['120677', '10310', '9876', '81199', '15781', '10712', '129994', '15101', '151463', '54668']}}
    resp = blog_writer.getBlogContent(x)
    print('--------------------------------------');
    print('resp=',resp);
    print('--------------------------------------');

    gpt_llm.add_message('user',resp)
    print('--------------------------------------');
    print('gpt_llm.conversation_history=',gpt_llm.conversation_history);
    print('--------------------------------------');
    response = await gpt_llm.chat_completion_request(gpt_llm.conversation_history, function_definitions.functions)
    full_msg = response.json()['choices'][0]

    def call_functions( full_msg):
        # messages = gpt_llm.conversation_history
        arguments = eval(full_msg['message']['function_call']['arguments'])
        print('--------------------------------------');
        print('arguments=',arguments);
        print('--------------------------------------');
        
        if full_msg['message']['function_call']['name']=="post_creator":
            try:
                
                result = wp_manager.post_creator(**arguments)
                print('--------------------------------------');
                print('result=',result);
                print('--------------------------------------');
                
                # response = await gpt_llm.chat_completion_request(messages)
            except Exception as e:
                print('--------------------------------------');
                print('erro in func call=',e);
                print('--------------------------------------');
    print('--------------------------------------');
    print('full_msg=',full_msg);
    print('--------------------------------------');
    
    if full_msg['finish_reason']=='function_call':
        function_name = response.json()['choices'][0]['message']['function_call']['name']
        print('--------------------------------------');
        print('function_name=',function_name);
        print('--------------------------------------');
        
        chat_response =  call_functions(full_msg)

    return "done"

# @router.post('/')
# async def post_todo(todo:Todo):
#     collection_name.insert_one(dict(todo))