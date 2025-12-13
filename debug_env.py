
import os
import sys

print("DEBUG: Python Environment Check")
print(f"MEGALLM_API_KEY present: {'MEGALLM_API_KEY' in os.environ}")
key = os.getenv('MEGALLM_API_KEY', '')
print(f"MEGALLM_API_KEY value: {key[:5]}...{key[-5:] if key else ''}")
print(f"MEGALLM_MODEL value: {os.getenv('MEGALLM_MODEL')}")
