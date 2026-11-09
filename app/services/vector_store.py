
from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "chroma"


def get_collection():
    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name="it_knowledge_base",
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    return collection
