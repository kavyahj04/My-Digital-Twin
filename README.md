# Digital Twin

A conversational "digital twin" chatbot that answers questions about Kavya Hosamane Jayanna's professional background — skills, work experience, education, and GitHub projects — as her portfolio assistant. It answers from a RAG knowledge base built from her GitHub repos and LinkedIn profile, and can capture visitor contact details when they want to be followed up with.

## How it works

1. A visitor chats with the assistant through the React frontend.
2. The FastAPI backend keeps a per-session message history and sends it to an LLM (via the OpenAI-compatible API) along with a system prompt that defines the twin's identity and scope.
3. The model can call tools to:
   - **`search_knowledge_base`** — semantic search over a Chroma vector store built from cleaned GitHub + LinkedIn data, to ground answers in real facts (with source citations).
   - **`collect_contact_info`** — record a visitor's name/email/phone/reason into a Google Sheet (via a service account) when they want to be contacted.
   - **`flag_off_topic`** — log attempts to extract the system prompt, jailbreak the assistant, or ask for private information outside its scope.
4. The reply (plus any cited sources) is returned to the frontend and rendered in the chat UI.

## Project structure

```
backend/
  main.py                 # FastAPI app: /chat and /health endpoints
  auth.py                 # GitHub OAuth routes
  embedding.py            # Builds the Chroma vector index from chunks.json
  chunk_builder.py        # Turns cleaned GitHub/LinkedIn data into RAG chunks
  prompts/sys_prompt.py   # System prompt defining the twin's identity, scope, and rules
  tools/
    knowledge_base.py     # search_knowledge_base tool (Chroma query)
    contact_info.py       # collect_contact_info tool (writes to Google Sheets)
    flag_message.py       # flag_off_topic tool (writes to flags.jsonl)
    tool_call_main.py     # Orchestrates the model + tool-calling loop

frontend/
  src/DigitalTwinChat.jsx # Main chat UI component
  ...                     # Vite + React app

rag/
  data_clean/             # Scripts to fetch and clean GitHub data
  data/                   # Cleaned JSON data, chunks.json, and the Chroma DB (my_vectordb/)
```

## Tech stack

- **Backend:** FastAPI, Pydantic, Uvicorn
- **LLM:** OpenAI-compatible chat completions API with function/tool calling (Groq used as a fallback/alt provider)
- **Vector store:** ChromaDB with OpenAI embeddings (`text-embedding-3-small`)
- **Leads storage:** Google Sheets via `gspread` + a Google service account
- **Frontend:** React 19 + Vite, `react-markdown` for rendering replies
- **Auth:** GitHub OAuth (for pulling repo data)

## Getting started

### Prerequisites

- Python 3.14
- Node.js (for the frontend)
- An OpenAI API key
- A Google Cloud service account with access to a target Google Sheet (for lead capture)
- A GitHub OAuth app (for pulling repo data into the knowledge base)

### 1. Configure environment variables

Create a `.env` file in the project root with:

```
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_REDIRECT_URI=
GROQ_API_KEY=
OPENAI_API_KEY=
GOOGLE_SHEETS_API=
GOOGLE_SERVICE_ACCOUNT_JSON=
LEADS_SHEET_ID=
```

`GOOGLE_SERVICE_ACCOUNT_JSON` should be the full service account JSON key as a single-line string.

### 2. Build the knowledge base

```bash
cd rag/data_clean
python store_github_data.py   # fetch + clean GitHub data
# provide cleaned linkedin_clean.json in rag/data/ separately

cd ../../backend
python chunk_builder.py       # build rag/data/chunks.json from cleaned data
python embedding.py           # index chunks into the Chroma vector store
```

### 3. Run the backend

```bash
cd backend
uv sync                       # or: pip install -e .
uvicorn main:app --reload
```

The API is served at `http://localhost:8000`, with `/chat` and `/health` endpoints.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

## API

### `POST /chat`

```json
{
  "session_id": "optional-existing-session-id",
  "message": "What projects has Kavya worked on?"
}
```

Returns:

```json
{
  "session_id": "uuid",
  "reply": "...",
  "sources": [{ "title": "...", "url": "...", "source_type": "github" }]
}
```

### `GET /health`

Returns `{"status": "ok"}`.

## Notes

- Conversation history per session is capped to the most recent turns to stay within the model provider's per-minute token limits.
- Never commit `.env` — it holds live API keys and service account credentials.
