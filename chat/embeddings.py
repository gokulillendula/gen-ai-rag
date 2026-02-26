import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# This finds the .env file in your rag_project folder, no matter where you run it from
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# This will now show the first 5 chars of your NEW key if found
print(f"DEBUG: Using key starting with: {GEMINI_API_KEY[:5] if GEMINI_API_KEY else 'None'}")

if not GEMINI_API_KEY:
    raise ValueError(f"Could not find GEMINI_API_KEY. Checked path: {env_path}")

client = genai.Client(api_key=GEMINI_API_KEY)
def get_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values