"""Compare baseline and passage reranking with full RAG generation.

Run from repository root:
    python -m scripts.evaluate_rerank_e2e --ids A01 A03 A07
    python -m scripts.evaluate_rerank_e2e

Reuses the existing evaluator and never overwrites final_mode_comparison.*.
Results are a curated development comparison, not a blinded test.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from scripts.compare_rag_modes import (
    DEFAULT_DATASET,
    DEFAULT_REPORT_DIR,
    evaluate_one,
    load_cases,
    render_markdown,
    summarize,
)

MODES = ("baseline", "rerank")


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline vs rerank end-to-end evaluation")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--ids", nargs="+", help="Only evaluate these case IDs, e.g. A01 A03 A07")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()

    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be in [1, 20]")

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    full_cases = load_cases(args.dataset)
    cases = full_cases
    if args.ids:
        available = {case["id"]: case for case in full_cases}
        missing = set(args.ids) - set(available)
        if missing:
            parser.error(f"Unknown case ID(s): {', '.join(sorted(missing))}")
        if len(set(args.ids)) != len(args.ids):
            parser.error("Duplicate IDs are not allowed")
        cases = [available[case_id] for case_id in args.ids]

    original_mode = os.environ.get("RAG_RETRIEVAL_MODE")
    rows = []
    try:
        for case in cases:
            for mode in MODES:
                print(f"Evaluating {case['id']} | {mode}", flush=True)
                row = evaluate_one(case, mode, args.top_k)
                rows.append(row)
                if row["error"]:
                    print(f"  ERROR: {row['error']}", flush=True)
                else:
                    print(
                        f"  Source hit={row['source_hit']}; citation IDs={row['citation_id_valid']}; "
                        f"refusal={row['correct_refusal']}; elapsed={row['elapsed_seconds']}s",
                        flush=True,
                    )
    finally:
        if original_mode is None:
            os.environ.pop("RAG_RETRIEVAL_MODE", None)
        else:
            os.environ["RAG_RETRIEVAL_MODE"] = original_mode

    summary = {
        mode: summarize([row for row in rows if row["mode"] == mode])
        for mode in MODES
    }
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": str(args.dataset),
        "dataset_size": len(full_cases),
        "cases_evaluated": len(cases),
        "modes": list(MODES),
        "top_k": args.top_k,
        "min_similarity": os.getenv("RAG_MIN_SIMILARITY", ""),
        "collection": "it_knowledge_base_v2",
        "rerank_candidates": os.getenv("RAG_RERANK_CANDIDATES", "80"),
        "rerank_lexical_weight": os.getenv("RAG_RERANK_LEXICAL_WEIGHT", "0.65"),
        "evaluation_scope": "Curated development set; not independent/blinded holdout",
        "summary": summary,
        "rows": rows,
    }

    suffix = "_" + "_".join(args.ids) if args.ids else ""
    base = "rerank_e2e_comparison" + suffix
    args.report_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.report_dir / f"{base}.json"
    md_path = args.report_dir / f"{base}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print("\n===== RERANK END-TO-END SUMMARY =====")
    for mode, metrics in summary.items():
        print(f"{mode}: {json.dumps(metrics, ensure_ascii=False)}")
    print("Reports:", json_path, md_path, sep="\n  ")


if __name__ == "__main__":
    main()
