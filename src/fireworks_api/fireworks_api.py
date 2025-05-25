import os
import fireworks.client
import dotenv
from dotenv import load_dotenv

dotenv_path = '../../env/.env'

load_dotenv(dotenv_path)
fireworks_api_key = os.getenv("FIREWORKS_API_KEY")

if not fireworks_api_key:
  raise ValueError("No API key found in the .env file. Please add your FIREWORKS_API_KEY to the .env file.")

fireworks.client.api_key = fireworks_api_key

def get_completion(prompt: str, model: str, max_tokens: int) -> str:
  completion = fireworks.client.Completion.create(
    model=model,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0
  )

  return completion.choices[0].text

models = [
  'accounts/fireworks/models/llama4-scout-instruct-basic', # $0.15 input, $0.60 output
  'accounts/fireworks/models/qwen3-30b-a3b', # $0.22 input, $0.60 output
  'accounts/fireworks/models/qwen3-235b-a22b', # $0.22 input, $0.88 output 
  'accounts/fireworks/models/deepseek-r1' # $3.00 input, $8.00 output
]