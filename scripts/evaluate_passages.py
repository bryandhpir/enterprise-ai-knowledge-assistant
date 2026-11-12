"""Compare baseline semantic retrieval vs optional lexical passage reranking.

Runs only local embeddings and ChromaDB. No Gemini calls, no index mutation.
Evaluation data is curated from previously reviewed cases, NOT blind holdout.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

from app.services.chroma_search import search_chroma
from app.services.lexical_reranker import retrieve_reranked

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evals" / "passage_eval_questions.json"
REPORT = ROOT / "evals" / "reports" / "passage_rerank_eval.json"


def first_rank(results: list[dict], expected: set[tuple[str, int]]) -> int | None:
    return next((i for i, item in enumerate(results, 1)
                 if (item["source"], item["chunk_index"]) in expected), None)


def report_mode(results: list[dict], row: dict, top_k: int) -> dict:
    expected_passages = {
        (item["source"], item["chunk_index"])
        for item in row["relevant_passages"]
    }
    rank = first_rank(results, expected_passages)
    return {
        "passage_first_rank": rank,
        "passage_hit": rank is not None and rank <= top_k,
        "source_hit": bool({r["source"] for r in results[:top_k]} &
                           set(row["relevant_sources"])),
        "top_results": [
            {"source": r["source"], "chunk_index": r["chunk_index"],
             "cosine_score": r["score"],
             **({"rerank_score": r["rerank_score"]} if "rerank_score" in r else {})}
            for r in results[:top_k]
        ],
    }


def main(dataset: Path, top_k: int, report: Path) -> None:
    if top_k < 1:
        raise ValueError("top_k must be positive")
    cases = json.loads(dataset.read_text(encoding="utf-8-sig"))
    if not cases:
        raise ValueError("Empty passage-level dataset")
    rows = []
    for item in cases:
        outputs = {"id": item["id"], "question": item["query"], "modes": {}}
        for mode in ("baseline", "rerank"):
            start = perf_counter()
            if mode == "baseline":
                chunks = search_chroma(item["query"], top_k=top_k,
                                       collection_name="it_knowledge_base_v2")
            else:
                chunks = retrieve_reranked(item["query"], top_k=top_k)
            entry = report_mode(chunks, item, top_k)
            entry["elapsed_seconds"] = round(perf_counter() - start, 3)
            outputs["modes"][mode] = entry
        rows.append(outputs)
        b = outputs["modes"]["baseline"]
        r = outputs["modes"]["rerank"]
        print(f"{item['id']}: baseline passage rank={b['passage_first_rank']}; "
              f"rerank passage rank={r['passage_first_rank']}")
        for mode in ("baseline", "rerank"):
            ids = [f"{x['source']}#{x['chunk_index']}" for x in outputs["modes"][mode]["top_results"]]
            print(f"  {mode:8}: {ids}")

    summary = {}
    for mode in ("baseline", "rerank"):
        evaluations = [x["modes"][mode] for x in rows]
        summary[mode] = {
            "cases": len(evaluations),
            "passage_hit_at_k": round(mean(x["passage_hit"] for x in evaluations), 4),
            "source_hit_at_k": round(mean(x["source_hit"] for x in evaluations), 4),
            "mrr_at_k": round(mean(1 / x["passage_first_rank"]
                                   if x["passage_first_rank"] else 0
                                   for x in evaluations), 4),
            "mean_retrieval_seconds": round(mean(x["elapsed_seconds"]
                                                 for x in evaluations), 3),
        }
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": str(dataset), "collection": "it_knowledge_base_v2",
        "top_k": top_k, "evaluation_scope": "Curated development cases; not independent holdout",
        "rerank_strategy": "BM25-style lexical scoring + original-query cosine on wider dense candidates",
        "summary": summary, "rows": rows,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n===== PASSAGE EVALUATION SUMMARY =====")
    for mode, metrics in summary.items():
        print(f"{mode.upper()}: " + " | ".join(f"{k}={v}" for k, v in metrics.items()))
    print("Saved:", report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    main(args.dataset, args.top_k, args.report)
