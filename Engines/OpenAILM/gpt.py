import openai
import os
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["model_name"] = "gpt-3.5-turbo-0613"


class GPTLLm:
    def __init__(self) -> None:
        self.conversation_history = []
        # self.model_name = "gpt-4-0613"
        # self.model_name = "gpt-3.5-turbo-0613"
        self.model_name = "gpt-3.5-turbo-1106"
        self.max_tokens = 3097
        self.max_tokens_instruct = 2097
        self.max_tokens_16k = 16385

    def add_message(self, role, content):
        content = str(content)
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def completion(self, prompt):
        try:            
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            response = openai.completions.create(
                # model=self.model_name,
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0.1,
                max_tokens=self.max_tokens_instruct,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response

        except Exception as e:
            print(f"\n\n Error in gpt completion --->: {e=}\n")
            
    def completion_batch(self, prompts):
        try:            
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompts,
                temperature=0.1,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response["choices"]
        except Exception as e:
            print(f"\n\n Error in gpt completion --->: {e=}\n")
            
    def chat_completion_request_sync(self, messages):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=self.max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response

    async def chat_completion_request(self, messages, functions=None):
        """
        call chat_completion endpoint with messages [], functions
        """
        model = self.model_name
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }

        # if conversation goes too long keep only last 5 messages
        if len(messages) > 5:
            system_msg = messages[0]
            messages_final = [system_msg]
            messages_final += messages[-5:]
            messages = messages_final

        json_data = {"model": model, "messages": messages, "temperature": 0.1}

        if functions is not None:
            json_data.update({"functions": functions})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=json_data,
                    timeout=30.0,
                )
                return response
        except Exception as e:
            print(f"Exception in chat_completion_request: {e}")
            return e

    def display_conversation(self):
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}\n\n")
