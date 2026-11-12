"""Optional, read-only continuation of selected V2 passages.

Only the immediate NEXT chunk in the SAME document AND SAME Markdown
section is appended. The anchor's original cosine score and rank are
unchanged. The additional passage is explicitly recorded in response
metadata so evidence is not misrepresented.
"""

import logging
import re

logger = logging.getLogger(__name__)
COLLECTION = "it_knowledge_base_v2"


def _get_collection():
    # Lazy import: offline unit tests do not require a ChromaDB install.
    from app.services.vector_store import get_collection
    return get_collection(name=COLLECTION)


def _heading(text: str) -> str | None:
    match = re.search(r"(?m)^Mục:\s*(.+?)\s*$", text)
    return match.group(1).strip().casefold() if match else None


def _passage_content(text: str) -> str | None:
    match = re.search(r"(?m)^Nội dung:\s*(.*)$", text, re.DOTALL)
    return match.group(1).strip() if match else None


def append_next_chunk_context(chunks: list[dict]) -> list[dict]:
    """Return copies of anchors enriched with one adjacent passage each.

    Chroma V2 uses IDs ``v2:<source>:<chunk_index>``. This method does not
    perform another vector search, alter rankings, or edit the index.
    If the volume cannot be read, the original chunks are returned unchanged.
    """
    if not chunks:
        return []

    anchors = [dict(item) for item in chunks]
    anchor_keys = {(item["source"], int(item["chunk_index"])) for item in chunks}

    candidates = {}
    for item in chunks:
        source = str(item["source"])
        index = int(item["chunk_index"])
        key = (source, index + 1)
        if key not in anchor_keys and _heading(item["text"]):
            candidates[f"v2:{source}:{index + 1}"] = key

    if not candidates:
        return anchors

    try:
        response = _get_collection().get(
            ids=list(candidates), include=["documents", "metadatas"]
        )
    except Exception as exc:
        logger.warning("Neighbor context unavailable; using anchors only: %s", exc)
        return anchors

    records = {}
    for id_value, text, metadata in zip(
        response.get("ids", []),
        response.get("documents") or [],
        response.get("metadatas") or [],
    ):
        if id_value in candidates and isinstance(text, str) and isinstance(metadata, dict):
            expected_source, expected_index = candidates[id_value]
            try:
                valid = (metadata.get("source") == expected_source and
                         int(metadata.get("chunk_index")) == expected_index)
            except (TypeError, ValueError):
                valid = False
            if valid:
                records[(expected_source, expected_index)] = text

    for item in anchors:
        source, index = str(item["source"]), int(item["chunk_index"])
        neighbor_text = records.get((source, index + 1))
        if not neighbor_text or _heading(item["text"]) != _heading(neighbor_text):
            continue
        body = _passage_content(neighbor_text)
        if not body:
            continue
        item["text"] = (
            item["text"] +
            f"\n\n[Adjacent context from the same section, chunk {index + 1}]\n" +
            body
        )
        item["context_chunk_indices"] = [index, index + 1]
    return anchors
