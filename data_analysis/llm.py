import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def llm_request(sys_prompt, usr_prompt, model="deepseek/deepseek-v3.2"):
    """
    OpenRouter LLM
    """
    # First API call with reasoning
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": sys_prompt
            },
            {
            "role": "user",
            "content": usr_prompt
            }
        ],
        "reasoning": {"enabled": True}
    })
    )
    
    # Extract the assistant message with reasoning_details
    response = response.json()
    response = response['choices'][0]['message']

    return response