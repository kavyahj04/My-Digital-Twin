import json
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv(override=True)

def load_chunks(path:str) -> list[dict]:
    return json.load(open(path, encoding="utf-8"))

def build_index(chunks:list[dict], persist_dir:str="my_vectordb"):
    client = chromadb.PersistentClient(path=persist_dir)
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-3-small")

    collection = client.get_or_create_collection(
        name = "digital-twin",
        embedding_function=embedding_fn
    )

    collection.add(
        ids = [f"{c['source_type']}-{i}" for i, c in enumerate(chunks)],
        documents = [c["text"] for c in chunks],
        metadatas = [
            {"source_type": c["source_type"], "entity_name" : c["entity_name"], "url":c["url"] or ""} for c in chunks
        ]
    )

    return collection

if __name__ == "__main__":
    chunks = load_chunks("../rag/data/chunks.json")
    collection = build_index(chunks)
    print(f"Indexed {collection.count()} chunks into chromadb")