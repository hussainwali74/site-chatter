from Tools.run_config import getRunConfig
from Tools.enums import ModelProvidersEnum 
class LLM:
    def __init__(self, model_name=ModelProvidersEnum.GEMINI):
        model = getRunConfig(model_name)
        self.model = model
        self.fast_model =getRunConfig(ModelProvidersEnum.COHERE)
        self.instruct_model =getRunConfig(ModelProvidersEnum.GEMINI)
        
    def generate_text(self, prompt):
        return self.model(prompt)
    def chat(self, messages):
        return self.model.chat(messages)

    def fast_generate(self, prompt):
        return self.fast_model(prompt)

    def instruct_generate(self, prompt):
        return self.instruct_model(prompt)