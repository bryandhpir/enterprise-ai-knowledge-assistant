"""Offline tests for same-section next-chunk context enrichment."""

from copy import deepcopy

from app.services import neighbor_context as nc


def chunk(source, index, heading, content, score=0.6):
    return {
        "source": source,
        "chunk_index": index,
        "text": f"Tài liệu: {source}\nMục: {heading}\nNội dung: {content}",
        "score": score,
    }


class FakeCollection:
    def __init__(self, records):
        self.records = records
        self.calls = []

    def get(self, ids, include):
        self.calls.append((ids, include))
        pairs = [(i, self.records[i]) for i in ids if i in self.records]
        return {
            "ids": [i for i, _ in pairs],
            "documents": [record["text"] for _, record in pairs],
            "metadatas": [
                {"source": record["source"], "chunk_index": record["chunk_index"]}
                for _, record in pairs
            ],
        }


def test_appends_next_same_section_and_preserves_anchor(monkeypatch):
    anchor = chunk("device_setup.md", 16, "Bước 5", "Đăng nhập và MFA")
    neighbor = chunk("device_setup.md", 17, "Bước 5", "Kiểm tra phần mềm bảo vệ")
    original = deepcopy(anchor)
    fake = FakeCollection({"v2:device_setup.md:17": neighbor})
    monkeypatch.setattr(nc, "_get_collection", lambda: fake)
    result = nc.append_next_chunk_context([anchor])
    assert "Kiểm tra phần mềm bảo vệ" in result[0]["text"]
    assert result[0]["context_chunk_indices"] == [16, 17]
    assert result[0]["score"] == 0.6
    assert result[0]["chunk_index"] == 16
    assert anchor == original
    assert fake.calls[0][1] == ["documents", "metadatas"]


def test_next_chunk_from_different_section_is_excluded(monkeypatch):
    fake = FakeCollection({"v2:doc.md:4": chunk("doc.md", 4, "Other heading", "Irrelevant")})
    monkeypatch.setattr(nc, "_get_collection", lambda: fake)
    result = nc.append_next_chunk_context([chunk("doc.md", 3, "Correct heading", "Answer")])
    assert "Irrelevant" not in result[0]["text"]
    assert "context_chunk_indices" not in result[0]


def test_no_fabrication_when_neighbor_missing(monkeypatch):
    monkeypatch.setattr(nc, "_get_collection", lambda: FakeCollection({}))
    c = chunk("doc.md", 16, "A", "Evidence")
    assert nc.append_next_chunk_context([c]) == [c]


def test_already_selected_neighbor_not_duplicate(monkeypatch):
    c16 = chunk("doc.md", 16, "A", "First")
    c17 = chunk("doc.md", 17, "A", "Second")
    fake = FakeCollection({"v2:doc.md:17": c17})
    monkeypatch.setattr(nc, "_get_collection", lambda: fake)
    result = nc.append_next_chunk_context([c16, c17])
    assert "Adjacent context" not in result[0]["text"]
    assert "v2:doc.md:17" not in fake.calls[0][0]


def test_mismatched_metadata_rejected(monkeypatch):
    class BadCollection:
        def get(self, ids, include):
            return {"ids": ids, "documents": [chunk("doc.md", 4, "A", "BAD")["text"]],
                    "metadatas": [{"source": "other.md", "chunk_index": 4}]}
    monkeypatch.setattr(nc, "_get_collection", lambda: BadCollection())
    result = nc.append_next_chunk_context([chunk("doc.md", 3, "A", "Valid")])
    assert "BAD" not in result[0]["text"]


def test_index_error_does_not_fail_rag(monkeypatch):
    def bad_collection():
        raise OSError("disk temporarily unavailable")
    monkeypatch.setattr(nc, "_get_collection", bad_collection)
    c = chunk("a.md", 1, "A", "Some content")
    assert nc.append_next_chunk_context([c]) == [c]


def test_empty_input():
    assert nc.append_next_chunk_context([]) == []


def test_separate_sections_and_multiple_anchors(monkeypatch):
    docs = {
        "v2:device_setup.md:17": chunk("device_setup.md", 17, "Bước 5", "Full checklist"),
        "v2:password_reset.md:15": chunk("password_reset.md", 15, "MFA", "IT identity verification"),
    }
    monkeypatch.setattr(nc, "_get_collection", lambda: FakeCollection(docs))
    a = chunk("device_setup.md", 16, "Bước 5", "Checklist part one")
    b = chunk("password_reset.md", 14, "MFA", "Lost phone")
    result = nc.append_next_chunk_context([a, b])
    assert result[0]["context_chunk_indices"] == [16, 17]
    assert result[1]["context_chunk_indices"] == [14, 15]
