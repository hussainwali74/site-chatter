from langchain.llms.base import LLM
import g4f
from langchain_g4f import G4FLLM

def llm(model):
    llm: LLM = G4FLLM(model=model)
    return llm

def chat(prompt, model=g4f.models.gpt_4o ):
    response = g4f.ChatCompletion.create(
        model=model,    
        messages=[{"role": "user", "content": prompt}],
        timeout=120,
        )
    return response