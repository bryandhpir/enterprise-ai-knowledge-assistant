from google.genai import errors
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_success(monkeypatch):
    calls = []

    def fake_answer_question(question, top_k):
        calls.append((question, top_k))

        return {
            "question": question,
            "answer": "Mở ứng dụng VPN. [S1]",
            "sources": [
                {
                    "id": "S1",
                    "source": "vpn_access.md",
                    "chunk_index": 6,
                    "score": 0.7898
                }
            ],
            "model": "mock-gemini"
        }

    monkeypatch.setattr(
        "app.main.answer_question",
        fake_answer_question
    )

    response = client.post(
        "/chat",
        json={
            "question": "  Làm thế nào để kết nối VPN?  ",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "Làm thế nào để kết nối VPN?"
    assert data["answer"] == "Mở ứng dụng VPN. [S1]"
    assert data["sources"][0]["id"] == "S1"
    assert data["sources"][0]["source"] == "vpn_access.md"
    assert data["model"] == "mock-gemini"

    assert calls == [("Làm thế nào để kết nối VPN?", 3)]

import pytest


@pytest.mark.parametrize(
    "request_body",
    [
        {"question": "   ", "top_k": 3},
        {"question": "VPN là gì?", "top_k": 0},
        {"question": "VPN là gì?", "top_k": 25},
        {"top_k": 3}
    ]
)
def test_chat_invalid_request(monkeypatch, request_body):

    def fake_answer_question(question, top_k):
        raise AssertionError(
            "RAG Service must not be called"
        )

    monkeypatch.setattr(
        "app.main.answer_question",
        fake_answer_question
    )

    response = client.post(
        "/chat",
        json=request_body
    )

    assert response.status_code == 422

def test_chat_gemini_api_error(monkeypatch):

    def fake_answer_question(question, top_k):
        raise errors.APIError(
            503,
            {"message": "Simulated Gemini service error"}
        )

    monkeypatch.setattr(
        "app.main.answer_question",
        fake_answer_question
    )

    response = client.post(
        "/chat",
        json={
            "question": "Làm thế nào để kết nối VPN?",
            "top_k": 3
        }
    )

    assert response.status_code == 502

    assert response.json() == {
        "detail": (
            "Dịch vụ AI hiện không khả dụng. "
            "Vui lòng thử lại sau."
        )
    }
