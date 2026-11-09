
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_documents():
    response = client.get("/documents")

    assert response.status_code == 200
    assert response.json()["total"] == 5

def test_search():
    response = client.get(
        "/search",
        params={"q": "mật khẩu"}
    )

    assert response.status_code == 200
    assert response.json()["total"] >= 1

def test_invalid_search():
    response = client.get(
        "/search",
        params={"q": "a"}
    )

    assert response.status_code == 422
