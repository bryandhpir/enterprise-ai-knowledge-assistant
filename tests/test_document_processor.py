
import pytest

from app.services.document_processor import (
    split_text,
    load_document_chunks
)


def test_split_text():
    text = " ".join(f"word{i}" for i in range(10))

    chunks = split_text(
        text,
        chunk_size=5,
        overlap=2
    )

    assert len(chunks) == 3

    assert chunks[0] == "word0 word1 word2 word3 word4"
    assert chunks[1] == "word3 word4 word5 word6 word7"


def test_empty_text():
    assert split_text("") == []


def test_invalid_overlap():
    with pytest.raises(ValueError):
        split_text("hello world", chunk_size=5, overlap=5)


def test_load_document_chunks():
    chunks = load_document_chunks()

    assert len(chunks) >= 5
    assert all(chunk["text"] for chunk in chunks)
    assert any(
        chunk["source"] == "password_reset.md"
        for chunk in chunks
    )
