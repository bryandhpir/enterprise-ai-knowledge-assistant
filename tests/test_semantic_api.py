
from fastapi.testclient import TestClient
import app.main as main_module

client = TestClient(main_module.app)


def fake_search(query: str, top_k: int = 3):
    return [
        {
            "source": "vpn_access.md",
            "chunk_index": i,
            "text": "Hướng dẫn kết nối VPN",
            "score": 0.75
        }
        for i in range(top_k)
    ]


def test_semantic_search_success(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "search_chroma",
        fake_search
    )

    response = client.post(
        "/semantic-search",
        json={
            "query": "Làm sao kết nối VPN?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["results"]) == 3
    assert data["results"][0]["source"] == "vpn_access.md"


def test_empty_query():
    response = client.post(
        "/semantic-search",
        json={"query": "", "top_k": 3}
    )

    assert response.status_code == 422


def test_whitespace_query():
    response = client.post(
        "/semantic-search",
        json={"query": "   ", "top_k": 3}
    )

    assert response.status_code == 422


def test_invalid_top_k():
    response = client.post(
        "/semantic-search",
        json={"query": "Kết nối VPN", "top_k": 0}
    )

    assert response.status_code == 422


def test_top_k_exceeds_limit():
    response = client.post(
        "/semantic-search",
        json={"query": "Kết nối VPN", "top_k": 21}
    )

    assert response.status_code == 422
