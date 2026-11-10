
import os
from pathlib import Path

from dotenv import load_dotenv

from app.services.vector_store import get_collection


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def is_ready() -> bool:
    # Check Gemini API key configuration
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return False

    # Check the V2 knowledge base
    collection = get_collection(
        name="it_knowledge_base_v2"
    )

    return collection.count() > 0
