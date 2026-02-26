import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# This finds the .env file in your rag_project folder, no matter where you run it from
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

# This will now show the first 5 chars of your NEW key if found
print(f"DEBUG: Using key starting with: {api_key[:] if api_key else 'None'}")

if not api_key:
    raise ValueError(f"Could not find GEMINI_API_KEY. Checked path: {env_path}")

client = genai.Client(api_key=api_key)
def get_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values