"""Focused, offline unit tests for optional passage reranking."""

import pytest
from app.services import lexical_reranker as lr


def chunk(source, index, text, score):
    return {"source": source, "chunk_index": index, "text": text, "score": score}


def test_specific_passage_beats_generic_higher_similarity():
    question = "VPN kết nối rồi nhưng không vào được phần mềm kế toán, cần làm gì?"
    rows = [
        chunk("vpn_access.md", 6, "Quy trình kết nối VPN Internet mở ứng dụng", 0.82),
        chunk("device_setup.md", 3, "Thiết bị cần Internet trước khi đăng nhập", 0.74),
        chunk("vpn_access.md", 22,
              "Kết nối VPN rồi nhưng không vào được hệ thống kế toán: "
              "kiểm tra quyền ứng dụng, gửi ticket cho IT", 0.53),
    ]
    ranked = lr.rerank_passages(question, rows, top_k=2)
    assert ranked[0]["source"] == "vpn_access.md"
    assert ranked[0]["chunk_index"] == 22
    assert ranked[0]["score"] == 0.53
    assert 0 <= ranked[0]["rerank_score"] <= 1


def test_original_candidate_dicts_not_modified():
    rows = [chunk("a.md", 1, "Bàn giao thiết bị IT", 0.56)]
    returned = lr.rerank_passages("bàn giao thiết bị", rows, top_k=1)
    assert "rerank_score" not in rows[0]
    assert "rerank_score" in returned[0]
    assert returned[0]["score"] == 0.56


def test_deduplicates_same_passage():
    rows = [
        chunk("a.md", 1, "IT kiểm tra thiết bị", 0.7),
        chunk("a.md", 1, "IT kiểm tra thiết bị", 0.7),
        chunk("b.md", 2, "VPN truy cập", 0.6),
    ]
    assert len(lr.rerank_passages("kiểm tra thiết bị", rows, top_k=3)) == 2


def test_no_lexical_overlap_keeps_dense_order():
    rows = [
        chunk("a.md", 1, "mật khẩu email", 0.85),
        chunk("b.md", 2, "cổng hỗ trợ", 0.60),
    ]
    ranked = lr.rerank_passages("xyzabc qwerty", rows, top_k=2)
    assert [r["source"] for r in ranked] == ["a.md", "b.md"]


def test_casefold_and_vietnamese_diacritics():
    assert lr._tokens("Quy TRÌNH cấp QUYỀN") == lr._tokens("quy trinh cap quyen")


def test_invalid_inputs():
    with pytest.raises(ValueError):
        lr.rerank_passages("  ", [], top_k=3)
    with pytest.raises(ValueError):
        lr.rerank_passages("VPN", [], top_k=0)
    with pytest.raises(ValueError):
        lr.rerank_passages("VPN", [], top_k=2, lexical_weight=1.2)
    assert lr.rerank_passages("VPN", [], top_k=2) == []


def test_retrieval_uses_larger_candidates_and_preserves_collection(monkeypatch):
    monkeypatch.delenv("RAG_RERANK_CANDIDATES", raising=False)
    monkeypatch.delenv("RAG_RERANK_LEXICAL_WEIGHT", raising=False)
    captured = []
    monkeypatch.setattr(lr, "search_chroma", lambda **kw: captured.append(kw) or [
        chunk("vpn_access.md", 22, "hệ thống kế toán VPN", 0.4)
    ])
    rows = lr.retrieve_reranked("kế toán VPN", top_k=3)
    assert captured[0]["top_k"] == 80
    assert captured[0]["collection_name"] == "it_knowledge_base_v2"
    assert rows[0]["source"] == "vpn_access.md"


def test_retrieval_supports_configurable_candidate_pool_and_weight(monkeypatch):
    monkeypatch.setenv("RAG_RERANK_CANDIDATES", "48")
    monkeypatch.setenv("RAG_RERANK_LEXICAL_WEIGHT", "0.4")
    captured = []
    monkeypatch.setattr(lr, "search_chroma", lambda **kw: captured.append(kw) or [
        chunk("vpn_access.md", 22, "kế toán VPN", 0.7)
    ])
    rows = lr.retrieve_reranked("kế toán VPN", top_k=3)
    assert captured[0]["top_k"] == 48
    assert rows[0]["source"] == "vpn_access.md"


def test_retrieval_rejects_bad_environment_settings(monkeypatch):
    monkeypatch.setenv("RAG_RERANK_CANDIDATES", "two hundred")
    with pytest.raises(ValueError, match="must be an integer"):
        lr.retrieve_reranked("kế toán VPN")
    monkeypatch.setenv("RAG_RERANK_CANDIDATES", "2")
    with pytest.raises(ValueError, match="between top_k"):
        lr.retrieve_reranked("kế toán VPN", top_k=3)
    monkeypatch.setenv("RAG_RERANK_CANDIDATES", "80")
    monkeypatch.setenv("RAG_RERANK_LEXICAL_WEIGHT", "1.5")
    with pytest.raises(ValueError, match="between 0 and 1"):
        lr.retrieve_reranked("kế toán VPN")
