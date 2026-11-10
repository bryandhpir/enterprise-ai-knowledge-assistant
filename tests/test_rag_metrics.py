
from evals.rag_metrics import (
    evaluate_case,
    summarize_results,
)

from app.services.rag_guardrails import NO_ANSWER


def test_correct_source_and_citation():
    case = {
        "id": "T01",
        "query": "Cách kết nối VPN?",
        "answerable": True,
        "relevant_sources": ["vpn_access.md"],
    }

    result = {
        "answer": "Mở ứng dụng VPN. [S1]",
        "sources": [
            {
                "id": "S1",
                "source": "vpn_access.md",
                "chunk_index": 6,
                "score": 0.85,
            }
        ],
    }

    row = evaluate_case(case, result)

    assert row["source_hit"] is True
    assert row["citation_valid"] is True


def test_invalid_citation():
    case = {
        "id": "T02",
        "query": "Cách kết nối VPN?",
        "answerable": True,
        "relevant_sources": ["vpn_access.md"],
    }

    result = {
        "answer": "Mở VPN. [S9]",
        "sources": [
            {
                "id": "S1",
                "source": "vpn_access.md",
                "chunk_index": 6,
                "score": 0.85,
            }
        ],
    }

    row = evaluate_case(case, result)

    assert row["source_hit"] is True
    assert row["citation_valid"] is False


def test_unanswerable_refusal():
    case = {
        "id": "T03",
        "query": "Cách nấu phở bò?",
        "answerable": False,
        "relevant_sources": [],
    }

    result = {
        "answer": NO_ANSWER,
        "sources": [],
    }

    row = evaluate_case(case, result)
    summary = summarize_results([row])

    assert row["refusal_correct"] is True
    assert summary["unanswerable_refusal_rate"] == 1.0
    assert summary["source_hit_rate"] is None
