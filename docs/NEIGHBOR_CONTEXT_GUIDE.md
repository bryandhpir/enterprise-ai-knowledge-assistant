# Neighboring Chunk Context — Optional RAG Experiment

## Goal

A03 and A07 sometimes return incomplete answers because relevant content continues
in the next V2 passage. Instead of modifying embeddings or the ChromaDB index,
this experiment appends the **immediately following chunk from the same Markdown
section** to each of the reranked Top-K passages.

The retrieval result list remains Top-K anchors; their ranks and similarity scores
are **not** recalculated. The API uses `context_chunk_indices` to identify the
additional evidence behind a citation. Streamlit displays the included indices.

## Configuration

Set in local `.env` (never commit secrets):

```dotenv
RAG_RETRIEVAL_MODE=rerank
RAG_RERANK_CANDIDATES=80
RAG_RERANK_LEXICAL_WEIGHT=0.65
RAG_CONTEXT_NEIGHBORS=false
```

The new option defaults to `false`. Set it to `true` only for experiments.
It is ignored in `baseline` and `multi_query` modes. No reindex is needed.

## Safety and correctness

- Only fetch `v2:<source>:<chunk_index+1>` by exact ID.
- Check returned source/index metadata and require an identical `Mục:` heading.
- Skip a candidate if the next passage was already selected among Top-K.
- Preserve the original retrieved passage and score; never assign a fabricated
  similarity score to a neighbor.
- Do not add neighbors as separate candidate results: they are supplementary
  evidence within the cited source span, disclosed via `context_chunk_indices`.
- If ChromaDB is unavailable, log a warning and fall back to original anchors.
- Evidence augmentation is **not authorization**; only use this prototype with
  fictional sample documents or data whose access has already been checked.

Limitations: the continuation is only one passage and may not contain the missing
answer; the same-heading rule cannot detect every topic shift. Longer prompts
may increase latency and Gemini cost. Source hit and citation ID validation do
not prove factual grounding or completeness.

## Offline tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Evaluation using Docker

After `docker compose up -d --build`, run:

```powershell
docker compose exec -T api python -m scripts.evaluate_neighbor_context --ids A03 A07
docker compose exec -T api python -m scripts.evaluate_neighbor_context
```

The second command writes new `neighbor_context_comparison.json` and `.md`
reports under `/app/evals/reports/` without overwriting previous reports.

Copy them back to Windows:

```powershell
docker compose cp api:/app/evals/reports/neighbor_context_comparison.json ./evals/reports/neighbor_context_comparison.json
docker compose cp api:/app/evals/reports/neighbor_context_comparison.md ./evals/reports/neighbor_context_comparison.md
```

Check A03 for identity verification / MFA recovery, and A07 for compliance and
endpoint-protection checks. Verify A01 and the four out-of-scope questions did
not regress. Compare exact answer contents, not just automated metrics.

This is still a curated development experiment; results are not a general
production accuracy guarantee.
