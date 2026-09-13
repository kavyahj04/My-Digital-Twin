from fastapi import FastAPI
from auth import router as auth_router
from pydantic import BaseModel
from tools.tool_call_main import run_converstion
from prompts.sys_prompt import SYSTEM_PROMPT
import uuid

app = FastAPI()
app.include_router(auth_router)

SESSIONS: dict[str, list[dict]] = {}

class ChatRequest(BaseModel):
    session_id : str | None = None
    message : str

class ChatResponse(BaseModel):
    session_id:str
    reply : str

@app.post("/chat", response_model=ChatResponse)
async def chat(request:ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = [{"role":"system", "content":SYSTEM_PROMPT}]
    
    SESSIONS[session_id].append({"role":"user", "content":request.message})
    reply = run_converstion(SESSIONS[session_id])
    print(SESSIONS)
    return ChatResponse(session_id=session_id, reply=reply)

@app.get("/health")
def health():
    return {"status": "ok"}