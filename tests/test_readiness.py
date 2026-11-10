
from fastapi.testclient import TestClient

from app.main import app
from app.services import readiness


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_success(monkeypatch):
    monkeypatch.setattr(
        "app.main.is_ready",
        lambda: True
    )

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_ready_unavailable(monkeypatch):
    monkeypatch.setattr(
        "app.main.is_ready",
        lambda: False
    )

    response = client.get("/ready")

    assert response.status_code == 503


def test_readiness_checks_collection(monkeypatch):
    monkeypatch.setenv(
        "GEMINI_API_KEY",
        "test-placeholder"
    )

    class FakeCollection:
        def count(self):
            return 10

    monkeypatch.setattr(
        readiness,
        "get_collection",
        lambda name: FakeCollection()
    )

    assert readiness.is_ready() is True
