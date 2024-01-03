import g4f
# BING ------------------------------------------------------------------------------------------------------------
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     # proxy="http://host:port",
#     # or socks5://user:pass@host:port
#     timeout=120, # in secs
# )
# 
# print(f"Result gpt_4:", response)
# BING ------------------------------------------------------------------------------------------------------------

# gpt3.5 ------------------------------------------------------------------------------------------------------------
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_35_long,
#     
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     # proxy="http://host:port",
#     # or socks5://user:pass@host:port
#     timeout=120, # in secs
# )
# print("-------------------------------------------------------------------------")
# print(f"{response=}")
# print("-------------------------------------------------------------------------")

# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_35_turbo_16k,
#     
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     # proxy="http://host:port",
#     # or socks5://user:pass@host:port
#     timeout=120, # in secs
# )
# print("-------------------------------------------------------------------------")
# print(f"{response=}")
# print("-------------------------------------------------------------------------")
# gpt3.5 ------------------------------------------------------------------------------------------------------------


# response = g4f.ChatCompletion.create(
#     model=g4f.models.claude_v2,
#     
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     # proxy="http://host:port",
#     # or socks5://user:pass@host:port
#     timeout=120, # in secs
# )
# print("-------------------------------------------------------------------------")
# print(f"{response=}")
# print("-------------------------------------------------------------------------")

# response = g4f.ChatCompletion.create(
#     model=g4f.models.mixtral_8x7b,
#     
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     # proxy="http://host:port",
#     # or socks5://user:pass@host:port
#     timeout=120, # in secs
# )
# print("-------------------------------------------------------------------------")
# print(f"{response=}")
# print("-------------------------------------------------------------------------")
# response = g4f.ChatCompletion.create(
#     model=g4f.models.llama2_70b,    
#     messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
#     timeout=120, # in secs
# )
# print("-------------------------------------------------------------------------")
# print(f"{response=}")
# print("-------------------------------------------------------------------------")
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_35_turbo,    
    messages=[{"role": "user", "content": "I know you are bing, but can you tell me what model are you. What is the underlying model? who are you? and what is your context window length?"}],
    timeout=120, # in secs,
    # provider=g4f.Provider.Bing
)
print("-------------------------------------------------------------------------")
print(f"{response=}")
print("-------------------------------------------------------------------------")
# g4f.models.gpt_35_turbo_16k