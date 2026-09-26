from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")
print(f"Key loaded: {key[:10]}...")

client = Groq(api_key=key)
models = client.models.list()
for m in models.data:
    print(m.id)