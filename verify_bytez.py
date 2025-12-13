
from bytez import Bytez
import os

key = "13ed3b2f261c6b84e4853944a01e814a"
sdk = Bytez(key)

print(f"Connecting to Bytez with key prefix: {key[:5]}...")

# choose Qwen3-4B-Instruct-2507
model_id = "Qwen/Qwen3-4B-Instruct-2507"
print(f"Loading model: {model_id}")
model = sdk.model(model_id)

# send input to model
try:
    print("Sending request...")
    output, error = model.run([
      {
        "role": "user",
        "content": "Hello! Are you working?"
      }
    ])
    
    print("-" * 30)
    print(f"Error: {error}")
    print(f"Output: {output}")
    print("-" * 30)
    
    if not error and output:
        print("✅ SUCCESS: Bytez integration working!")
    else:
        print("❌ FAILURE: Bytez returned error or empty output")
        
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
