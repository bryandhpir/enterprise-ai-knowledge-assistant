
import pytest

from evals.metrics import retrieval_metrics


def test_relevant_document_at_rank_two():

    results = [
        {"source": "security_policy.md"},
        {"source": "vpn_access.md"},
        {"source": "device_setup.md"}
    ]

    metrics = retrieval_metrics(
        results,
        ["vpn_access.md"],
        k=3
    )

    assert metrics["hit"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["rr"] == 0.5


def test_relevant_document_not_in_top_three():

    results = [
        {"source": "password_reset.md"},
        {"source": "security_policy.md"},
        {"source": "device_setup.md"},
        {"source": "vpn_access.md"}
    ]

    metrics = retrieval_metrics(
        results,
        ["vpn_access.md"],
        k=3
    )

    assert metrics["hit"] == 0.0
    assert metrics["recall"] == 0.0
    assert metrics["rr"] == 0.0


def test_multiple_relevant_documents():

    results = [
        {"source": "vpn_access.md"},
        {"source": "vpn_access.md"},
        {"source": "security_policy.md"}
    ]

    metrics = retrieval_metrics(
        results,
        ["vpn_access.md", "security_policy.md"],
        k=3
    )

    assert metrics["hit"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["rr"] == 1.0


def test_invalid_k():
    with pytest.raises(ValueError):
        retrieval_metrics([], ["vpn_access.md"], k=0)
