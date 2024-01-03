import cohere 
import os
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv('COHERE_API_KEY')) # This is your trial API key

def cohereLLM(message):
    response = co.chat( 
            model='command',
            message=message,
            temperature=0,
            chat_history=[],
            prompt_truncation='AUTO',
            stream=False,
        ) 
    return response.text