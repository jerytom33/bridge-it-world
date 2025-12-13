
import os
from openai import OpenAI
import time

api_key = "sk-mega-51c1ea28e101197977ad76e5d4446be7fdc5d0e2f45a92060e4d82a8d4c51839"
base_url = "https://ai.megallm.io/v1"

models = ["gpt-3.5-turbo", "gpt-4o-mini"]

client = OpenAI(api_key=api_key, base_url=base_url)

print("--- START TEST ---")
for model in models:
    print(f"Testing {model}...")
    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"PASS: {model}")
    except Exception as e:
        print(f"FAIL: {model} - {str(e)}")
print("--- END TEST ---")
