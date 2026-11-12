# Passage Reranking Configuration

The `rerank` mode retrieves dense candidates from ChromaDB V2, then reranks them with lexical BM25-style scoring plus original-query cosine similarity.

Configuration (add to local `.env`):

```dotenv
RAG_RETRIEVAL_MODE=rerank
RAG_RERANK_CANDIDATES=80
RAG_RERANK_LEXICAL_WEIGHT=0.65
```

The current reranking defaults are **80 candidates** and **0.65 lexical weight**. `RAG_RETRIEVAL_MODE` still defaults to `baseline` unless explicitly enabled. The changes do not modify the ChromaDB index, any query expansion code, or Docker Compose.

These parameters were selected from **eight curated development cases**, where Passage Hit@3 reached 8/8 and known H12 source rank reached 3. They should not be presented as production accuracy or a generalization guarantee. MRR@3 on these cases was 0.7917. Increasing the dense candidate pool can increase retrieval work and latency.

The script `scripts.evaluate_passages` evaluates the `rerank` mode through `retrieve_reranked`; it now exercises the same candidate-pool setting as the deployed API. When comparing latency, warm the embedding model and repeat measurements.

Test commands:

```powershell
.\.venv\Scripts\python.exe -m pytest -q

docker compose up -d --build
docker compose exec -T api python -m scripts.evaluate_passages
```

Verify the effective mode and configuration inside Docker:

```powershell
docker compose exec -T api python -c "import os; print({k: os.getenv(k) for k in ('RAG_RETRIEVAL_MODE','RAG_RERANK_CANDIDATES','RAG_RERANK_LEXICAL_WEIGHT')})"
```

When changes are made to `.env`, recreate the container with `docker compose up -d --force-recreate`. Do not use `docker compose down -v`; that would remove the vector and model-cache volumes.
