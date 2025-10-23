from groq import Groq
from langchain.chat_models import init_chat_model

from config.config import *

client = Groq(api_key=GROQ_API_KEY)

def groq_chat(messages, model=MODEL_NAME, temperature=0.2) -> str:
    '''
    Groq chat completion
    '''
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        # reasoning_format='raw',
        # reasoning_effort="medium",
    )
    return resp.choices[0].message.content



# Initialize Groq model
model = init_chat_model(
    "groq:" + MODEL_NAME, 
    api_key=GROQ_API_KEY,
    temperature=0.2
)