import cohere 
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

co = cohere.Client(os.getenv('COHERE_API_KEY') or os.getenv('CO_API_KEY')) # This is your trial API key

def cohereLLM(message):
    response = co.chat( 
            model='command-r-plus',
            message=message,
            temperature=0,
            chat_history=[],
            prompt_truncation='AUTO',
        ) 
    return response.text