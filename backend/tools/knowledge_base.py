from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv(override=True)

SEARCH_KNOWLEDGE_BASE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": (
            "Search Kavya's background knowledge base - her GitHub projects and LinkedIn "
            "professional history - to answer questions about her skills, work experience, "
            "education, or projects. Call this whenever a visitor asks something requiring "
            "specific facts about her; never answer such questions from guesswork. You may "
            "call this more than once in a turn with different queries if one search doesn't "
            "fully cover the question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A focused search phrase, e.g. 'Python experience' or 'RAG chatbot "
                        "projects' - not the visitor's raw message verbatim."
                    ),
                },
                "n_results": {
                    "type": "integer",
                    "description": "How many results to retrieve. Defaults to 5; use more for broad questions. less if you could not find 5,",
                },
            },
            "required": ["query"],
        },
    },
}

VECTORDB_PATH = Path(__file__).resolve().parent.parent / "my_vectordb"

client = chromadb.PersistentClient(path=str(VECTORDB_PATH))
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-3-small")
collection = client.get_collection("digital-twin", embedding_function=embedding_fn)

def search_knowledge_base(query:str, n_results:int=5) -> dict:
    results = collection.query(query_texts=[query], n_results=n_results)
    matches = [
        {"source": meta["entity_name"],
        "source_type" : meta["source_type"],
        "content" : doc
        }
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]
    return {"query":query, "results": matches}