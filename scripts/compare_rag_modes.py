"""Compare baseline vs optional multi-query RAG end to end.

From repository root:
    python -m scripts.compare_rag_modes --limit 2
    python -m scripts.compare_rag_modes

No ChromaDB modifications; the retrieval mode is changed only in this process.
This is a curated challenge set, NOT a blinded holdout or production benchmark.
"""

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "evals" / "final_eval_questions.json"
DEFAULT_REPORT_DIR = BASE_DIR / "evals" / "reports"
MODES = ("baseline", "multi_query")


def load_cases(path: Path) -> list[dict]:
    cases = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("Evaluation dataset must be a nonempty JSON array")
    ids = set()
    for case in cases:
        if not isinstance(case, dict) or not all(
            key in case for key in ("id", "query", "answerable", "relevant_sources")
        ):
            raise ValueError("Each case needs id, query, answerable, relevant_sources")
        if case["id"] in ids:
            raise ValueError(f"Duplicate case id: {case['id']}")
        ids.add(case["id"])
        if not isinstance(case["query"], str) or not case["query"].strip():
            raise ValueError(f"Empty query for {case['id']}")
        if not isinstance(case["answerable"], bool):
            raise ValueError(f"answerable must be bool for {case['id']}")
        if not isinstance(case["relevant_sources"], list):
            raise ValueError(f"relevant_sources must be a list for {case['id']}")
        if case["answerable"] and not case["relevant_sources"]:
            raise ValueError(f"Missing relevant sources for {case['id']}")
        if not case["answerable"] and case["relevant_sources"]:
            raise ValueError(f"Unanswerable case has sources for {case['id']}")
    return cases


def evaluate_one(case: dict, mode: str, top_k: int) -> dict:
    from app.services.rag_service import answer_question
    from evals.rag_metrics import evaluate_case

    os.environ["RAG_RETRIEVAL_MODE"] = mode
    start = time.perf_counter()
    try:
        result = answer_question(case["query"], top_k=top_k)
        elapsed = round(time.perf_counter() - start, 3)
        metrics = evaluate_case(case, result)
        return {
            "id": case["id"],
            "question": case["query"],
            "mode": mode,
            "answerable": case["answerable"],
            "expected_sources": case["relevant_sources"],
            "review_focus": case.get("review_focus", ""),
            "elapsed_seconds": elapsed,
            "source_hit": metrics["source_hit"],
            "citation_id_valid": metrics["citation_valid"],
            "correct_refusal": metrics["refusal_correct"],
            "citation_failed": metrics["citation_failed"],
            "answer": result["answer"],
            "sources": result["sources"],
            "model": result["model"],
            "error": None,
            "manual_review": {
                "grounded": "not_assessed",
                "complete": "not_assessed",
                "claim_citations_supported": "not_assessed",
                "notes": "",
            },
        }
    except Exception as exc:
        elapsed = round(time.perf_counter() - start, 3)
        return {
            "id": case["id"],
            "question": case["query"],
            "mode": mode,
            "answerable": case["answerable"],
            "expected_sources": case["relevant_sources"],
            "review_focus": case.get("review_focus", ""),
            "elapsed_seconds": elapsed,
            "source_hit": None,
            "citation_id_valid": None,
            "correct_refusal": None,
            "citation_failed": None,
            "answer": None,
            "sources": [],
            "model": None,
            "error": f"{type(exc).__name__}: {exc}",
            "manual_review": {
                "grounded": "not_assessed",
                "complete": "not_assessed",
                "claim_citations_supported": "not_assessed",
                "notes": "",
            },
        }


def summarize(rows: list[dict]) -> dict:
    answerable = [r for r in rows if r["answerable"]]
    unanswerable = [r for r in rows if not r["answerable"]]

    def fraction(items, key):
        if not items:
            return None
        # Error rows contribute zero successes; never silently drop failures.
        return round(sum(r[key] is True for r in items) / len(items), 4)

    return {
        "total": len(rows),
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
        "errors": sum(bool(r["error"]) for r in rows),
        "source_hit_rate": fraction(answerable, "source_hit"),
        "citation_id_valid_rate": fraction(answerable, "citation_id_valid"),
        "correct_refusal_rate": fraction(unanswerable, "correct_refusal"),
        "average_latency_seconds": round(mean(r["elapsed_seconds"] for r in rows), 3)
        if rows else None,
    }


def as_percent(value):
    return "N/A" if value is None else f"{100 * value:.1f}%"


def as_bool(value):
    return "Pass" if value is True else "Fail" if value is False else "N/A"


def render_markdown(report: dict) -> str:
    modes = report["modes"]
    summary = report["summary"]
    rows = report["rows"]
    lines = [
        "# End-to-End RAG Mode Comparison", "",
        f"Generated UTC: {report['generated_at']}",
        f"Dataset: `{report['dataset']}` ({report['cases_evaluated']} of {report['dataset_size']} cases)",
        f"Retrieval collection: `{report['collection']}`; Top-K: {report['top_k']}",
        f"Similarity threshold: `{report['min_similarity'] or 'disabled'}`", "",
        "> This is an additional curated challenge set. It is not an independent or blinded holdout.",
        "> Model generation and query expansion can vary between runs.", "",
        "## Automated metrics", "",
        "| Metric | " + " | ".join(modes) + " |",
        "| --- | " + " | ".join("---:" for _ in modes) + " |",
    ]
    metrics = [
        ("Source Hit Rate (answerable)", "source_hit_rate", True),
        ("Valid Citation ID Rate (answerable)", "citation_id_valid_rate", True),
        ("Correct Refusal Rate (unanswerable)", "correct_refusal_rate", True),
        ("Average latency (seconds; all cases)", "average_latency_seconds", False),
        ("Errors", "errors", False),
    ]
    for label, key, is_percent in metrics:
        values = []
        for mode in modes:
            value = summary[mode][key]
            values.append(as_percent(value) if is_percent else str(value))
        lines.append(f"| {label} | " + " | ".join(values) + " |")

    lines.extend(["", "## Per-case results", "",
                  "| Case | Mode | Source Hit | Citation IDs | Refusal | Latency (s) | Error |",
                  "| --- | --- | --- | --- | --- | ---: | --- |"])
    for row in rows:
        error = (row["error"] or "-").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {row['id']} | {row['mode']} | {as_bool(row['source_hit'])} "
            f"| {as_bool(row['citation_id_valid'])} | {as_bool(row['correct_refusal'])} "
            f"| {row['elapsed_seconds']:.3f} | {error} |"
        )

    lines.extend([
        "", "## Manual answer review — not yet performed", "",
        "Inspect each generated answer against the relevant document passage, then fill in the JSON",
        "`manual_review` fields. The `review_focus` field provides a starting point, not an automated verdict.",
        "", "| Case | Mode | Grounded | Complete | Claim citations supported |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(f"| {row['id']} | {row['mode']} | Not assessed | Not assessed | Not assessed |")

    lines.extend([
        "", "## Interpretation limits", "",
        "- Source Hit uses filenames, not passage-level relevance.",
        "- A valid citation ID is not proof that a statement is supported.",
        "- The correct-refusal metric checks an exact configured no-answer response.",
        "- Failure rows count as unsuccessful for success-rate denominators.",
        "- The saved JSON includes generated answers and returned source metadata for manual inspection.",
        "- This run does not cache generated variants or assess whether query rewrites preserved intent.",
        "- Neither result establishes production reliability, authorization, or protection of private data.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare RAG retrieval modes end to end")
    parser.add_argument("--mode", choices=("both", *MODES), default="both")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()
    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be between 1 and 20")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")

    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
    cases = load_cases(args.dataset)
    total = len(cases)
    if args.limit is not None:
        cases = cases[:args.limit]
    modes = list(MODES) if args.mode == "both" else [args.mode]
    before_mode = os.environ.get("RAG_RETRIEVAL_MODE")
    rows = []
    try:
        for case in cases:
            for mode in modes:
                print(f"Evaluating {case['id']} | {mode}", flush=True)
                row = evaluate_one(case, mode, args.top_k)
                rows.append(row)
                if row["error"]:
                    print(f"  ERROR: {row['error']}", flush=True)
                else:
                    print(f"  Source hit: {row['source_hit']} | "
                          f"Citation IDs: {row['citation_id_valid']} | "
                          f"Refusal: {row['correct_refusal']} | "
                          f"Latency: {row['elapsed_seconds']}s", flush=True)
    finally:
        if before_mode is None:
            os.environ.pop("RAG_RETRIEVAL_MODE", None)
        else:
            os.environ["RAG_RETRIEVAL_MODE"] = before_mode

    summary = {mode: summarize([r for r in rows if r["mode"] == mode]) for mode in modes}
    preview = len(cases) < total
    suffix = f"_preview_{len(cases)}" if preview else ""
    base = "final_mode_comparison" + suffix
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": str(args.dataset),
        "dataset_size": total,
        "cases_evaluated": len(cases),
        "modes": modes,
        "top_k": args.top_k,
        "min_similarity": os.getenv("RAG_MIN_SIMILARITY", ""),
        "collection": "it_knowledge_base_v2",
        "evaluation_scope": "Curated challenge set, not independent/blinded holdout",
        "summary": summary,
        "rows": rows,
    }
    args.report_dir.mkdir(parents=True, exist_ok=True)
    json_file = args.report_dir / f"{base}.json"
    md_file = args.report_dir / f"{base}.md"
    json_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_file.write_text(render_markdown(report), encoding="utf-8")
    print("\n===== FINAL SUMMARY =====")
    for mode, stats in summary.items():
        print(f"{mode}: {json.dumps(stats, ensure_ascii=False)}")
    print("Reports:", json_file, md_file, sep="\n  ")


if __name__ == "__main__":
    main()
