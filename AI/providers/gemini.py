import os
import PIL.Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  # This is your API key

# Define text model
def geminiProTextLLM(message):
    model = genai.GenerativeModel('gemini-pro')
    generation_config = genai.GenerationConfig(max_output_tokens=8000)
    response = model.generate_content(message, generation_config=generation_config)
    return response.text

# Define text and image model
def geminiProVisionLLM(message, image_path):
    img = PIL.Image.open(image_path)
    model = genai.GenerativeModel('gemini-pro-vision',generation_config={'max_output_tokens':8000})
    response = model.generate_content([message, img])
    return response.text