import json
import os
# Import the client and get_embedding function from your embeddings file
from .embeddings import get_embedding, client 
from .vector_store import vector_store, search

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/docs.json")

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_and_index():
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}")
        return

    with open(DATA_PATH, "r") as f:
        documents = json.load(f)

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            embedding = get_embedding(chunk)
            vector_store.append({
                "title": doc["title"],
                "chunk": chunk,
                "embedding": embedding
            })

def generate_answer(question, history):
    query_embedding = get_embedding(question)
    retrieved = search(query_embedding)

    if not retrieved:
        return ("I don't have enough information to answer that.", 0, [])

    context = "\n\n".join([r[1]["chunk"] for r in retrieved])

    # New SDK Prompting logic using the client
    prompt = f"""
    You are a helpful AI assistant.
    Answer ONLY using the context below.
    If the answer is not in the context, say currently unavailable and answer using your general knowledge.

    Context:
    {context}

    Conversation History:
    {history}

    Question:
    {question}
    """

    # Using client.models.generate_content instead of genai.GenerativeModel
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
        }
    )
    reply = response.text
    tokens_used = (
        response.usage_metadata.total_token_count
        if hasattr(response, "usage_metadata")
        else 0
    )

    return reply, tokens_used, retrieved