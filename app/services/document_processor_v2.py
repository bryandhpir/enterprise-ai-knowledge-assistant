
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = BASE_DIR / "sample_docs"


def split_long_paragraph(
    text: str,
    max_words: int = 45,
    overlap: int = 8
) -> list[str]:

    if max_words <= 0:
        raise ValueError("max_words must be positive")

    if not 0 <= overlap < max_words:
        raise ValueError("Invalid overlap")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_words, len(words))

        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks


def load_document_chunks_v2() -> list[dict]:
    all_chunks = []

    for file_path in sorted(DOCS_DIR.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")

        document_title = file_path.stem.replace("_", " ")
        current_heading = document_title
        paragraph_lines = []
        chunk_index = 0

        def flush_paragraph():
            nonlocal chunk_index

            paragraph = " ".join(paragraph_lines).strip()
            paragraph_lines.clear()

            if not paragraph:
                return

            parts = split_long_paragraph(paragraph)

            for part in parts:
                enriched_text = (
                    f"Tài liệu: {document_title}\n"
                    f"Mục: {current_heading}\n"
                    f"Nội dung: {part}"
                )

                all_chunks.append({
                    "id": f"v2:{file_path.name}:{chunk_index}",
                    "source": file_path.name,
                    "chunk_index": chunk_index,
                    "text": enriched_text
                })

                chunk_index += 1

        for line in content.splitlines():
            stripped = line.strip()

            if re.match(r"^#{1,6}\s+", stripped):
                flush_paragraph()
                current_heading = re.sub(
                    r"^#{1,6}\s+", "", stripped
                ).strip()

            elif not stripped:
                flush_paragraph()

            else:
                paragraph_lines.append(stripped)

        flush_paragraph()

    return all_chunks
