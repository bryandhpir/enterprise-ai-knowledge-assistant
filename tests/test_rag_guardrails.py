
from app.services import rag_service

from app.services.rag_guardrails import (
    filter_chunks,
    citations_are_valid,
    NO_ANSWER,
)


def test_filter_chunks():
    chunks = [
        {"text": "VPN", "score": 0.85},
        {"text": "Email", "score": 0.40},
    ]

    result = filter_chunks(
        chunks,
        min_score=0.70
    )

    assert len(result) == 1
    assert result[0]["text"] == "VPN"


def test_citation_validation():
    sources = [
        {"id": "S1"},
        {"id": "S2"}
    ]

    assert citations_are_valid(
        "Mở VPN [S1] và đăng nhập [S2].",
        sources
    )

    assert not citations_are_valid(
        "Mở VPN [S3].",
        sources
    )

    assert not citations_are_valid(
        "Mở VPN.",
        sources
    )


def test_no_answer_skips_gemini(monkeypatch):
    monkeypatch.setenv(
        "RAG_MIN_SIMILARITY",
        "0.80"
    )

    def fake_search(**kwargs):
        return [
            {
                "text": "Unrelated document",
                "score": 0.30,
                "source": "sample.md",
                "chunk_index": 0
            }
        ]

    monkeypatch.setattr(
        rag_service,
        "search_chroma",
        fake_search
    )

    result = rag_service.answer_question(
        "Câu hỏi ngoài phạm vi?"
    )

    assert result["answer"] == NO_ANSWER
    assert result["sources"] == []
    assert result["model"] is None
