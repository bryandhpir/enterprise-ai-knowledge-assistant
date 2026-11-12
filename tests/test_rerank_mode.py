"""Feature flag route: rerank mode must not change the default baseline."""

from app.services import rag_service
from app.services.rag_guardrails import NO_ANSWER


def test_rerank_mode_dispatches_and_skips_gemini_with_no_evidence(monkeypatch):
    from app.services import lexical_reranker
    calls = []
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "rerank")
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "")
    monkeypatch.setattr(lexical_reranker, "retrieve_reranked",
                        lambda question, top_k: calls.append((question, top_k)) or [])
    result = rag_service.answer_question("Thiết bị không hoạt động", top_k=3)
    assert result["answer"] == NO_ANSWER
    assert result["sources"] == []
    assert calls == [("Thiết bị không hoạt động", 3)]


def test_baseline_remains_default(monkeypatch):
    calls = []
    monkeypatch.delenv("RAG_RETRIEVAL_MODE", raising=False)
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "")
    monkeypatch.setattr(rag_service, "search_chroma",
                        lambda **kw: calls.append(kw) or [])
    assert rag_service.answer_question("Truy cập VPN")["answer"] == NO_ANSWER
    assert calls[0]["collection_name"] == "it_knowledge_base_v2"
