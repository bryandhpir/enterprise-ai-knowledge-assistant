
from app.services.rag_guardrails import (
    NO_ANSWER,
    UNVERIFIED_ANSWER,
    citations_are_valid,
)


def evaluate_case(case: dict, result: dict) -> dict:
    answer = result["answer"].strip()
    sources = result["sources"]
    answerable = case["answerable"]

    returned_sources = {
        source["source"] for source in sources
    }

    expected_sources = set(
        case["relevant_sources"]
    )

    source_hit = (
        bool(returned_sources & expected_sources)
        if answerable else None
    )

    citation_valid = (
        citations_are_valid(answer, sources)
        if answerable else None
    )

    refusal_correct = (
        answer == NO_ANSWER
        if not answerable else None
    )

    return {
        "id": case["id"],
        "question": case["query"],
        "answerable": answerable,
        "source_hit": source_hit,
        "citation_valid": citation_valid,
        "refusal_correct": refusal_correct,
        "citation_failed": answer == UNVERIFIED_ANSWER,
        "answer": answer,
        "sources": sources,
    }


def calculate_rate(rows: list[dict], key: str):
    values = [
        row[key]
        for row in rows
        if row[key] is not None
    ]

    if not values:
        return None

    return round(
        sum(values) / len(values), 4
    )


def summarize_results(rows: list[dict]) -> dict:
    return {
        "total": len(rows),
        "answerable_cases": sum(
            row["answerable"] for row in rows
        ),
        "unanswerable_cases": sum(
            not row["answerable"] for row in rows
        ),
        "source_hit_rate": calculate_rate(
            rows, "source_hit"
        ),
        "citation_id_valid_rate": calculate_rate(
            rows, "citation_valid"
        ),
        "unanswerable_refusal_rate": calculate_rate(
            rows, "refusal_correct"
        ),
    }
