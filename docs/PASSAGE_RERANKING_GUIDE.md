# Passage-Level Reranking Experiment

## Purpose

The earlier end-to-end review found document-level source hits without the passage required to answer, notably:

- **A01:** `vpn_access.md`, chunk 22, accounting application access despite VPN connectivity.
- **A03:** `password_reset.md`, chunks 14–15, lost MFA device.
- **A07:** `device_setup.md`, chunk 16, IT equipment checks prior to handover.

This patch adds an **optional, lightweight lexical reranker**, not a new large neural model. It keeps current `baseline` and `multi_query` modes intact and leaves `baseline` as the default.

### Implementation

1. Stage 1: query the existing `it_knowledge_base_v2` ChromaDB collection and request a wider dense candidate pool (48 by default, capped at 80).
2. Stage 2: tokenize Vietnamese text with lightweight accent folding, compute BM25-style lexical relevance within candidate chunks, and combine a normalized lexical score (weight 0.65) with the normalized cosine similarity to the original question (weight 0.35).
3. Return up to `top_k` passages. Keep `score` as the original-query cosine similarity; store the new ranking signal in `rerank_score`. The existing `RAG_MIN_SIMILARITY` guardrail still uses cosine similarity, not the reranking score.

**Important limitations:** The tokenization uses whitespace and Unicode normalization rather than full Vietnamese word segmentation. Candidate expansion and reranking may increase CPU work and can make some queries worse. This approach cannot recover a passage that does not appear among the dense candidates. The reranker is not a cross-encoder; it makes no claim to be one.

## Files to place into the project

```text
app/services/lexical_reranker.py   # New
app/services/rag_service.py       # Replace existing file (adds rerank feature flag)
tests/test_lexical_reranker.py     # New
tests/test_rerank_mode.py         # New
evals/passage_eval_questions.json # New, curated passage-level labels
scripts/evaluate_passages.py      # New
```

Do not overwrite your existing multi-query experiment, reports, vector database, or Docker volumes. Make changes on `feat/multi-query-retrieval` or a new experiment branch.

## Validate before rebuilding Docker

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Then rebuild using cache (no `--no-cache`):

```powershell
docker compose up -d --build
docker compose exec -T api python -m pytest -q
```

## Run passage-level evaluation (does NOT call Gemini)

```powershell
docker compose exec -T api python -m scripts.evaluate_passages
```

Output is written inside the API container to `evals/reports/passage_rerank_eval.json`. Retrieve it to Windows:

```powershell
docker compose cp api:/app/evals/reports/passage_rerank_eval.json evals/reports/passage_rerank_eval.json
```

The report prints and saves **passage_hit_at_k**, **source_hit_at_k**, **mrr_at_k**, and **mean_retrieval_seconds**, separately for `baseline` and `rerank`. Labels are curated from previously reviewed cases; this is not a blind independent holdout. The `chunk_index` labels refer to the present V2 Markdown chunker and must be checked again if the source documents or chunking rules change.

Inspect A01, A03, A07 first. If the exact passages still fail to appear, consider a larger candidate pool, lexical retrieval on the whole small corpus, or a neural cross-encoder reranker; do not claim the current approach solves the issue before measurement.

## Try the feature flag only after reviewing metrics

In `.env`:

```dotenv
RAG_RETRIEVAL_MODE=rerank
```

Recreate containers so the new environment setting takes effect:

```powershell
docker compose up -d --force-recreate
```

Ask the chatbot A01 and A07, as well as the previously difficult H12 question. Also recheck all unanswerable cases. Restore the default by setting `RAG_RETRIEVAL_MODE=baseline` and recreating containers; no index rebuild is required. Baseline should remain the default until answer quality, refusal behavior and latency have been measured on fresh cases.

## Evaluation cautions

- **Document/source hit** does not mean the relevant passage was provided.
- **Passage hit** does not mean Gemini used it correctly.
- **Citation ID valid** does not mean claim-level attribution is supported.
- Rerank-score is **not** a probability, cosine similarity, or calibrated confidence threshold.
- This lexical reranker uses **existing embeddings** and does **not** require another model download.
- This package is experimental and should not be described as production-secure retrieval.
