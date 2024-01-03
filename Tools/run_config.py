from g4f import models

from AI.providers.cohere import cohereLLM
from AI.providers.gemini import geminiProTextLLM
from AI.providers import g4f_llm
from Tools.enums import ModelProvidersEnum

run_config = {
    ModelProvidersEnum.G4F:{
        "writer_model":[
            {"model":models.gpt_4_32k_0613,"status":0, "limit":2048, "rating":9},
            {"model":models.gpt_4_32k,"status":0, "limit":2048, "rating":10},
            {"model":models.gpt_35_turbo,"status":0, "limit":2048, "rating":9},
            ],
        "instruct":[
            {"model":models.gpt_35_turbo,"status":0, "limit":2048, "rating":9},
        ]
    },
    ModelProvidersEnum.COHERE:{
        "writer_model":[
            {"model":cohereLLM,"status":0, "limit":2048, "rating":9},
        ]
    },
    ModelProvidersEnum.GEMINI:{
        "writer_model":[
            {"model":geminiProTextLLM,"status":0, "limit":4048, "rating":9},
        ]
    },
    ModelProvidersEnum.OPENAI:{
        "writer_model":[
            {"model":models.gpt_4_32k_0613,"status":0, "limit":2048, "rating":9},
        ],
        
    }
}
def getRunConfig(model_name, type='writer_model'):
    model = run_config[model_name].get(type)[0].get('model')
    if model_name==ModelProvidersEnum.G4F:
        return g4f_llm.chat
    return model
