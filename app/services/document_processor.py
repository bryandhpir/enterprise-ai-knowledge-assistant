
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = BASE_DIR / "sample_docs"


def split_text(
    text: str,
    chunk_size: int = 60,
    overlap: int = 20
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if not 0 <= overlap < chunk_size:
        raise ValueError("Invalid overlap")

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks

def load_document_chunks() -> list[dict]:

    all_chunks = []

    for file_path in sorted(DOCS_DIR.glob("*.md")):

        content = file_path.read_text(
            encoding="utf-8"
        )

        chunks = split_text(content)

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "id": f"{file_path.name}:{index}",
                "source": file_path.name,
                "chunk_index": index,
                "text": chunk
            })

    return all_chunks
