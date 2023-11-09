from Engines.OpenAILM import gpt
from Engines.Writer import prompts
gpt = gpt.GPTLLm()

def getBlogContent(data):
    # data = {'channel_details': [{'channelName': 'MR. INDIAN HACKER', 'url': 'https://www.youtube.com/@mrindianhacker', 'subscriberCount': '33500000', 'viewCount': '6010457396', 'videoCount': '947', 'playlist_id': 'UUSiDGb0MnHFGjs4E2WKvShw'}], 'videos_details': {'Title': ["World's Biggest Rocket Wheel - Will It Work ? | 1000 Rockets", 'Biggest Diwali Dhamaka - 100% Real', 'अजीबो गरीब पटाखे - Testing New Diwali Crackers | Diwali Stash 2023', 'All New Fireworks - Biggest Diwali Stash 2023 | कीमत - ₹ 1000000000000000000000000000000000000000000', 'Finally!  रावण का किया अंत | Happy Dussehra 2023', 'Ravan Ki Lanka - रावण का महल मिल गया | Dussehra Special', 'We Make Big Toy Train - हमारी खुद की रेलगाड़ी | 🚂', 'Human Electricity Generator - 100% Working | Science Project', 'Desi Water Filter System - ₹2000 Only...पूरे तालाब का पानी साफ़ करेगा', 'Meet Our Dada Ji...Challenge भारी पड़ गया 😂'], 'commentCount': ['8068', '16677', '10862', '21243', '11622', '19732', '19611', '14387', '16148', '18197']}}
    # prompt= prompts.getBlogTemplate('fun tech', data['channel_details'],data['videos_details'])
    prompt = prompts.channelReviewPrompt(data)
    gpt.add_message('system',"prompt")
    response =  gpt.completion(prompt)
    return response.choices[0].text
