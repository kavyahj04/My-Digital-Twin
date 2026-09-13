from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from openai import APIStatusError
from pydantic import BaseModel
from tools.tool_call_main import run_converstion
from prompts.sys_prompt import SYSTEM_PROMPT
import uuid

# Groq's free tier caps at 8000 tokens/minute, so the conversation sent to the
# model is capped to the most recent turns to keep growing sessions from
# blowing past that limit and triggering a 429.
MAX_HISTORY_MESSAGES = 12

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)

SESSIONS: dict[str, list[dict]] = {}

class ChatRequest(BaseModel):
    session_id : str | None = None
    message : str

class ChatResponse(BaseModel):
    session_id:str
    reply : str

@app.post("/chat", response_model=ChatResponse)
def chat(request:ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = [{"role":"system", "content":SYSTEM_PROMPT}]

    SESSIONS[session_id].append({"role":"user", "content":request.message})

    # keep the system prompt plus only the most recent turns
    history = SESSIONS[session_id]
    if len(history) > MAX_HISTORY_MESSAGES + 1:
        SESSIONS[session_id] = [history[0], *history[-MAX_HISTORY_MESSAGES:]]

    try:
        reply = run_converstion(SESSIONS[session_id])
    except APIStatusError as e:
        # covers both 429 (rate limit) and 413 (request too large for the
        # TPM cap) - both stem from the same per-minute token ceiling
        print(f"chat rate-limit error: {e}")
        reply = "I'm getting a lot of questions right now and hit a rate limit. Please wait a few seconds and try again."
    except Exception as e:
        print(f"chat error: {e}")
        reply = "Something went wrong on my end processing that. Please try again."

    return ChatResponse(session_id=session_id, reply=reply)

@app.get("/health")
def health():
    return {"status": "ok"}