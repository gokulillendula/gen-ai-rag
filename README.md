Production-Grade GenAI Assistant with RAG

📌 Overview

This project implements a production-style GenAI-powered Chat Assistant using Retrieval-Augmented Generation (RAG).

The assistant retrieves relevant document chunks using embedding-based semantic search and generates grounded responses using Gemini LLM.

The system operates in strict RAG mode to prevent hallucinations.

🏗 Architecture Diagram
<img width="1881" height="564" alt="Screenshot (19)" src="https://github.com/user-attachments/assets/6292626b-7b3a-4966-8b75-154abee21670" />

🔄 RAG Workflow Explanation

1️⃣ Indexing Phase (Runs at Server Startup)
  •	Load docs.json
  
  •	Split documents into chunks (~400 words with overlap)
  
  •	Generate embeddings using Gemini embedding model

  •	Store embeddings in in-memory vector store
  
  •	This happens once when the server starts.


2️⃣ Query Phase (Runs Per Request)
When a user sends a message:
1.	Generate embedding for user query
2.	Perform cosine similarity search
3.	Retrieve top 3 most relevant chunks
4.	Apply similarity threshold (0.6)
5.	If no relevant chunks → return fallback
6.	Inject retrieved context into structured prompt
7.	Generate response using Gemini LLM

Embedding Strategy

•	Model used: gemini-embedding-001

•	Each document is chunked before embedding

•	Each chunk gets its own embedding vector

•	Why chunking?

•	Improves retrieval precision

•	Prevents injecting large irrelevant documents

•	Optimizes context window usage

📊Similarity Search Explanation

Cosine similarity formula:

similarity = (A · B) / (||A|| ||B||)

Why cosine similarity?

•	Measures semantic closeness between vectors

•	Standard in embedding-based systems

•	Efficient and scalable

Top 3 chunks are selected with threshold filtering to ensure relevance.

📝 Prompt Design Reasoning

Prompt used:
You are a helpful AI assistant.
Answer ONLY using the context below.
If the answer is not in the context, say you don't know.

Context:
{retrieved_chunks}

Conversation History:
{last_3_message_pairs}

Question:
{user_query}

Design Decisions:

Strict grounding prevents hallucination

Explicit instruction to avoid external knowledge

Short conversation memory (3 pairs)

Low temperature (0.2) for deterministic answers

🔒 Hallucination Prevention

Embedding-based retrieval (no keyword search)

Similarity threshold filtering

Strict fallback response

Controlled temperature (0.2)

If similarity score is too low:

"I don't have enough information to answer that."

🔌 API Endpoint

POST /chat/

Request
{
  "sessionId": "abc123",
  "message": "How can I reset my password?"
}

Response

{
  "reply": "Users can reset their password from Settings > Security...",
  "tokensUsed": 132,
  "retrievedChunks": 2
}

⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone <your_repo_url>

cd gen-ai-assistant

2️⃣ Create Virtual Environment

python -m venv venv

venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Add Gemini API Key

Create .env file:

GEMINI_API_KEY=your_api_key_here

5️⃣ Run Server

python manage.py runserver

Open:

http://127.0.0.1:8000/

🖥 Frontend Features

•	Chat UI

•	Session handling via localStorage

•	Loading indicator

•	Message history display

•	Scroll to bottom

🚀 Features Implemented

•	Real embedding-based retrieval

•	Cosine similarity search

•	Threshold filtering

•	Strict RAG mode

•	Token usage tracking

•	Session-based memory

•	Clean Django API


Session-based memory

Clean Django API

Interactive chat frontend
