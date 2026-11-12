"""Compare rerank with vs without same-section continuation.

Run from project root:
  python -m scripts.evaluate_neighbor_context --ids A03 A07
  python -m scripts.evaluate_neighbor_context

Writes unique reports, preserving all prior baseline/rerank evaluations.
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

MODES = ("rerank_original", "rerank_with_neighbors")


def main():
    parser = argparse.ArgumentParser(description="Evaluate optional neighboring passages")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--ids", nargs="+", help="Limit to case IDs, e.g. A03 A07")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()
    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be between 1 and 20")

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    full_cases = load_cases(args.dataset)
    cases = full_cases
    if args.ids:
        labels = {item["id"]: item for item in full_cases}
        if len(set(args.ids)) != len(args.ids) or any(i not in labels for i in args.ids):
            parser.error("Duplicate or unknown case IDs")
        cases = [labels[i] for i in args.ids]

    original_mode = os.environ.get("RAG_RETRIEVAL_MODE")
    original_neighbors = os.environ.get("RAG_CONTEXT_NEIGHBORS")
    rows = []
    try:
        for case in cases:
            for mode, enabled in ((MODES[0], False), (MODES[1], True)):
                os.environ["RAG_CONTEXT_NEIGHBORS"] = "true" if enabled else "false"
                print(f"Evaluating {case['id']} | {mode}", flush=True)
                # evaluate_one sets the retrieval mode in THIS process only.
                row = evaluate_one(case, "rerank", args.top_k)
                row["mode"] = mode
                rows.append(row)
                print(
                    f"  source_hit={row['source_hit']} citation_ids={row['citation_id_valid']} "
                    f"refusal={row['correct_refusal']} latency={row['elapsed_seconds']}s "
                    f"error={row['error'] or '-'}",
                    flush=True,
                )
    finally:
        if original_mode is None:
            os.environ.pop("RAG_RETRIEVAL_MODE", None)
        else:
            os.environ["RAG_RETRIEVAL_MODE"] = original_mode
        if original_neighbors is None:
            os.environ.pop("RAG_CONTEXT_NEIGHBORS", None)
        else:
            os.environ["RAG_CONTEXT_NEIGHBORS"] = original_neighbors

    summary = {mode: summarize([r for r in rows if r["mode"] == mode]) for mode in MODES}
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
        "evaluation_scope": "Same curated development set; not independent/blinded holdout",
        "summary": summary,
        "rows": rows,
    }
    args.report_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_" + "_".join(args.ids) if args.ids else ""
    base = "neighbor_context_comparison" + suffix
    json_path = args.report_dir / f"{base}.json"
    md_path = args.report_dir / f"{base}.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md = render_markdown(report).replace(
        "Model generation and query expansion can vary between runs.",
        "Model generation can vary between runs. Neighboring chunks are deterministic."
    )
    md_path.write_text(md, encoding="utf-8")
    print("\n===== NEIGHBOR CONTEXT EVALUATION SUMMARY =====")
    for mode, metrics in summary.items():
        print(f"{mode}: {json.dumps(metrics, ensure_ascii=False)}")
    print("Reports:", json_path, md_path, sep="\n  ")


if __name__ == "__main__":
    main()
