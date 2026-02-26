
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .rag_pipeline import generate_answer
from django.shortcuts import render

def home(request):
    return render(request, "chats.html")
sessions = {}

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_id = data.get("sessionId")
        message = data.get("message")

        if not message:
            return JsonResponse({"error": "Message required"}, status=400)

        history = sessions.get(session_id, [])

        reply, tokens_used, retrieved = generate_answer(message, history)

        history.append(("user", message))
        history.append(("assistant", reply))

        sessions[session_id] = history[-6:]  

        return JsonResponse({
    "reply": reply,
    "tokensUsed": tokens_used,
    "retrievedChunks": len(retrieved)
})