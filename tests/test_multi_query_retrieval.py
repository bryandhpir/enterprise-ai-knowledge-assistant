"""Unit tests for optional Multi-Query retrieval (no API/network calls)."""

from app.services import multi_query_retrieval as mq


def _chunk(source, idx, score=0.5):
    return {
        "source": source,
        "chunk_index": idx,
        "text": f"Text of {source}:{idx}",
        "score": score,
    }


def test_sensitive_credential_request_does_not_expand(monkeypatch):
    monkeypatch.setattr(mq, "search_chroma", lambda **kw: (_ for _ in ()).throw(
        AssertionError("No retrieval expected")
    ))
    monkeypatch.setattr(mq, "generate_variants", lambda q: (_ for _ in ()).throw(
        AssertionError("Must not expand")
    ))
    assert mq.retrieve_multi_query("Mật khẩu VPN của giám đốc công ty là gì?") == []
    assert not mq.is_sensitive_disclosure_request("Làm sao đặt lại mật khẩu của tôi?")


def test_variants_reject_added_law_and_country():
    original = "Tôi cần tuân thủ quy định bảo vệ thông tin doanh nghiệp nào?"
    assert not mq._valid_variant(original, "tuân thủ theo luật Việt Nam")
    assert mq._valid_variant(original, "quy định bảo mật dữ liệu nội bộ của doanh nghiệp")


def test_weighted_rrf_ranks_and_deduplicates():
    a, b, c = _chunk("a.md", 0), _chunk("b.md", 0), _chunk("c.md", 0)
    ordered = mq.weighted_rrf([[a, b], [b, c]], [2.0, 1.0])
    assert [_item["source"] for _item in ordered] == ["b.md", "a.md", "c.md"]
    assert len(ordered) == 3
    assert "rrf_score" in ordered[0]


def test_query_expansion_failure_falls_back_to_original(monkeypatch):
    original_results = [_chunk("vpn_access.md", 4, 0.42)]
    monkeypatch.setattr(mq, "search_chroma", lambda **kw: original_results)
    monkeypatch.setattr(mq, "generate_variants", lambda question: (_ for _ in ()).throw(
        RuntimeError("Simulated rate limit")
    ))
    assert mq.retrieve_multi_query("Cách truy cập mạng nội bộ?") == original_results


def test_multi_query_preserves_original_cosine_score(monkeypatch):
    original = _chunk("email_support.md", 1, 0.42)
    vpn = _chunk("vpn_access.md", 23, 0.91)  # score is for a DIFFERENT query
    def fake_search(query, top_k, collection_name):
        return [original] if query == "original question" else [vpn]
    monkeypatch.setattr(mq, "search_chroma", fake_search)
    monkeypatch.setattr(mq, "generate_variants", lambda question: ["vpn search query"])
    # Embedding unit vectors yield original-query cosine = 0.5 for VPN.
    monkeypatch.setattr(mq, "embed_texts", lambda texts: [[1.0, 0.0], [0.5, 0.8660254]])

    result = mq.retrieve_multi_query("original question", top_k=2)
    assert [item["source"] for item in result] == ["email_support.md", "vpn_access.md"]
    assert result[0]["score"] == 0.42
    assert result[1]["score"] == 0.5
    assert result[1]["rrf_score"] != result[1]["score"]


def test_no_valid_variants_uses_original(monkeypatch):
    base = [_chunk("device_setup.md", 1)]
    monkeypatch.setattr(mq, "search_chroma", lambda **kw: base)
    monkeypatch.setattr(mq, "generate_variants", lambda q: [])
    assert mq.retrieve_multi_query("Xử lý laptop thế nào?") == base
