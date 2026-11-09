
from app.services.document_processor_v2 import (
    load_document_chunks_v2,
    split_long_paragraph
)


def test_split_long_paragraph():
    text = " ".join(f"word{i}" for i in range(20))

    chunks = split_long_paragraph(
        text,
        max_words=10,
        overlap=2
    )

    assert len(chunks) == 3
    assert chunks[0].split()[-2:] == chunks[1].split()[:2]


def test_v2_chunks_have_metadata():
    chunks = load_document_chunks_v2()

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk["source"]
        assert chunk["id"]
        assert "Tài liệu:" in chunk["text"]
        assert "Mục:" in chunk["text"]
        assert "Nội dung:" in chunk["text"]
