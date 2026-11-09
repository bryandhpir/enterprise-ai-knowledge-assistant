
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")


def main():
    client = genai.Client(api_key=api_key)

    response = client.interactions.create(
        model=model_name,
        input="Giải thích RAG là gì bằng tiếng Việt trong 2 câu."
    )

    if not response.output_text:
        raise RuntimeError("Gemini returned no text")

    print("Model:", model_name)
    print("Gemini response:")
    print(response.output_text)


if __name__ == "__main__":
    main()
