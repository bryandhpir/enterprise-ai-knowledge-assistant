"""Integration test for the optional RAG feature flag; Gemini is mocked."""

from types import SimpleNamespace

from app.services import rag_service, neighbor_context


def test_context_expansion_enabled_in_rerank_only(monkeypatch):
    from app.services import lexical_reranker

    def anchor():
        return {"source": "device_setup.md", "chunk_index": 16,
                "text": "Tài liệu: device setup\nMục: Bước 5\nNội dung: Login",
                "score": 0.53}

    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "rerank")
    monkeypatch.setenv("RAG_CONTEXT_NEIGHBORS", "true")
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "")
    monkeypatch.setenv("GEMINI_API_KEY", "fake")
    monkeypatch.setattr(lexical_reranker, "retrieve_reranked", lambda question, top_k: [anchor()])
    monkeypatch.setattr(neighbor_context, "append_next_chunk_context", lambda chunks: [
        {**chunks[0], "text": chunks[0]["text"] + "\nMore checklist",
         "context_chunk_indices": [16, 17]}
    ])

    seen_prompts = []

    class Client:
        def __init__(self, api_key):
            assert api_key == "fake"
            self.interactions = SimpleNamespace(create=self.create)

        def create(self, model, input):
            seen_prompts.append(input)
            return SimpleNamespace(output_text="Bước kiểm tra gồm đăng nhập và bảo vệ thiết bị [S1].")

    monkeypatch.setattr(rag_service.genai, "Client", Client)
    response = rag_service.answer_question("IT kiểm tra gì?", top_k=3)
    assert "More checklist" in seen_prompts[0]
    assert response["sources"][0]["context_chunk_indices"] == [16, 17]
    assert response["sources"][0]["score"] == 0.53


def test_feature_off_avoids_expansion(monkeypatch):
    from app.services import lexical_reranker
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "rerank")
    monkeypatch.setenv("RAG_CONTEXT_NEIGHBORS", "false")
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "0.9")
    monkeypatch.setattr(lexical_reranker, "retrieve_reranked", lambda question, top_k: [
        {"source": "test.md", "chunk_index": 3, "text": "short", "score": 0.1}
    ])
    monkeypatch.setattr(neighbor_context, "append_next_chunk_context",
                        lambda chunks: (_ for _ in ()).throw(AssertionError("must not expand")))
    assert rag_service.answer_question("Test case")["sources"] == []
