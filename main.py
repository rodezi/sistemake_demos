from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv 

load_dotenv(".env")
app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "gpt-3.5-turbo" 

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Retell AI - Text Agent is alive"}

@app.post("/chat")
async def chat(request: Request):
    """Chat endpoint to interact with the language model."""
    data = await request.json()
    user_input = data.get("message", "")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": user_input}],
        },
    )

    reply = response.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
