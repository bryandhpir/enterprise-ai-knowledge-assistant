"""Feature-flag behavior tests. Tests do not call Google Gemini."""

import pytest

from app.services import rag_service
from app.services.rag_guardrails import NO_ANSWER


def test_baseline_remains_default(monkeypatch):
    monkeypatch.delenv("RAG_RETRIEVAL_MODE", raising=False)
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "")
    calls = []
    def fake_search(**kwargs):
        calls.append(kwargs)
        return []
    monkeypatch.setattr(rag_service, "search_chroma", fake_search)
    result = rag_service.answer_question("Không có dữ liệu phù hợp")
    assert result["answer"] == NO_ANSWER
    assert calls[0]["collection_name"] == "it_knowledge_base_v2"


def test_multi_query_mode_skips_gemini_when_no_sources(monkeypatch):
    from app.services import multi_query_retrieval as mq
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "multi_query")
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "")
    monkeypatch.setattr(mq, "retrieve_multi_query", lambda question, top_k: [])
    result = rag_service.answer_question("Mật khẩu VPN của giám đốc là gì?")
    assert result["answer"] == NO_ANSWER
    assert result["sources"] == []
    assert result["model"] is None


def test_unknown_mode_rejected(monkeypatch):
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "unknown")
    with pytest.raises(ValueError, match="RAG_RETRIEVAL_MODE"):
        rag_service.answer_question("Câu hỏi hợp lệ")
