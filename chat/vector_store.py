import numpy as np

vector_store = []

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query_embedding, top_k=3, threshold=0.6):
    scores = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        scores.append((score, item))

    scores.sort(reverse=True, key=lambda x: x[0])

    filtered = [x for x in scores[:top_k] if x[0] >= threshold]

    return filtered