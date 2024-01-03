import requests

url = "http://182.176.4.137:8080/v1/chat/completions"

def llm(prompt):
    messages = [
        {"role":"system","content":"you are an expert writer. You pay special attention to the user's requested output format."},
        {"role":"user","content":prompt}
    ]

    data = {"mode": "chat", "character": "Assistant", "messages": messages}

    response = requests.post(url, json=data)
    assistant_message = response.json()['choices'][0]['message']['content']
    # messages.append({"role": "assistant", "content": assistant_message})
    return assistant_message

    

# while True:
#     user_message = input("> ")
#     history.append({"role": "user", "content": user_message})
#     data = {
#         "mode": "chat",
#         "character": "Example",
#         "messages": history
#     }
# 
#     response = requests.post(url, headers=headers, json=data, verify=False)
#     assistant_message = response.json()['choices'][0]['message']['content']
#     history.append({"role": "assistant", "content": assistant_message})
#     print(assistant_message)


# import requests
# 
# # Base URL of the API
# base_url = "http://182.176.4.137:8080"
# 
# # Endpoint for generating text
# endpoint = "/v1/completions"
# 
# # Data to send to the API
# data = {
#    "prompt": "This is a cake recipe:\n\n1.",
#    "max_tokens": 200,
#    "temperature": 1,
#    "top_p": 0.9,
#    "seed": 10
# }
# 
# # Send a POST request to the API
# response = requests.post(f"{base_url}{endpoint}", json=data)
# 
# # Print the response
# print(response.json())
