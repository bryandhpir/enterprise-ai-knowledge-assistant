
import re


NO_ANSWER = (
    "Tôi không tìm thấy đủ thông tin "
    "trong tài liệu được cung cấp."
)

UNVERIFIED_ANSWER = (
    "Tôi chưa thể tạo câu trả lời "
    "có trích dẫn nguồn hợp lệ."
)


def filter_chunks(
    chunks: list[dict],
    min_score: float | None = None
) -> list[dict]:

    return [
        chunk
        for chunk in chunks
        if chunk["text"].strip()
        and (
            min_score is None
            or chunk["score"] >= min_score
        )
    ]


def citations_are_valid(
    answer: str,
    sources: list[dict]
) -> bool:

    cited_ids = set(
        re.findall(r"\[(S\d+)\]", answer)
    )

    valid_ids = {
        source["id"]
        for source in sources
    }

    return bool(cited_ids) and cited_ids.issubset(valid_ids)
