# End-to-End RAG Evaluation Guide

This evaluation compares the same newly curated challenge questions under the original
`baseline` retrieval and the optional `multi_query` retrieval. The corpus is still the
five fictional IT guides. Do not present these results as an independent holdout study.

## Prerequisites

- `multi_query_retrieval.py` and updated `rag_service.py` are installed.
- Docker Compose is running and the V2 ChromaDB collection is indexed.
- An approved Gemini API key is configured in `.env` (never commit it).
- The two new files are placed at `evals/final_eval_questions.json` and
  `scripts/compare_rag_modes.py`.

The runner changes `RAG_RETRIEVAL_MODE` **only in its own Python process**. It does
not modify `.env`, the running FastAPI process, or any ChromaDB collections.

## Run with Docker

Copy the source files into the running container without rebuilding the image:

```powershell
docker compose cp evals/final_eval_questions.json api:/app/evals/final_eval_questions.json
docker compose cp scripts/compare_rag_modes.py api:/app/scripts/compare_rag_modes.py
```

For a short smoke test:

```powershell
docker compose exec -T api python -m scripts.compare_rag_modes --limit 2
```

For the complete comparison:

```powershell
docker compose exec -T api python -m scripts.compare_rag_modes
```

Results are written to `evals/reports/final_mode_comparison.json` and `.md` **inside
that container**. Copy them to Windows:

```powershell
docker compose cp api:/app/evals/reports/final_mode_comparison.json evals/reports/final_mode_comparison.json
docker compose cp api:/app/evals/reports/final_mode_comparison.md evals/reports/final_mode_comparison.md
```

For a limited smoke test, filenames include `_preview_2` instead.

## Metrics and review

- `source_hit_rate`: expected source filename is in top-K retrieved sources.
- `citation_id_valid_rate`: generated answer mentions existing source IDs.
- `correct_refusal_rate`: response equals the canonical no-answer text.
- `average_latency_seconds`: observed elapsed time per question, including the model/API.
- Failed requests count as failures rather than disappearing from metrics.

These automated checks do **not** prove factual groundedness or completeness. For
answerable cases, manually compare the answer with supporting source text and record
whether all key points were covered and whether each cited source supports its claim.

A `review_focus` field in the dataset is only a reviewer prompt. The evaluation
script intentionally does not use it as an automatic judge.

## Practical limitations

- This set was authored after earlier failure analysis, so do not claim it is unseen
  production data or independent evidence of model generalization.
- Several questions can legitimately map to more than one source; this dataset lists
  acceptable source filenames for source-level evaluation only.
- Query expansion introduces nondeterminism, latency and extra Gemini API requests.
- The evaluation does not log generated query variants or detect fallback-to-baseline.
- Four unanswerable examples are not a comprehensive security evaluation.
- The model may provide an answer with correctly formatted citations that are still
  unsupported by the actual passages.
