import re
from OpenAILM.gpt import GPTLLm

def get_completion_answer(prompt):
    gpt_llm = GPTLLm()
    answer = gpt_llm.completion(prompt)
    if len(answer):
        import re
        answer=re.sub(r'\n',' ', answer)
    res = str(answer).strip()  
    flags = re.MULTILINE|re.IGNORECASE
    res = re.sub('^virtual assistant:', '', res, flags=flags)  
    return res

def get_completion_answer_batch(prompts):
    gpt_llm = GPTLLm()
    choices = gpt_llm.completion_batch(prompts)
    print(f"\n\n choices --->: {choices=}\n")
    
    # if len(choices):

    #     import re
    #     answer=re.sub(r'\n',' ', answer)
    # res = str(answer).strip()  
    # flags = re.MULTILINE|re.IGNORECASE
    # res = re.sub('^virtual assistant:', '', res, flags=flags)  
    # return res
