# Optional Multi-Query Retrieval

This experimental strategy is **off by default**. It supplements the original
`it_knowledge_base_v2` retrieval with two Gemini-generated search rewrites and
weighted Reciprocal Rank Fusion (RRF). Only the original question is passed to
the final answer-generation prompt.

## Configuration

Add to `.env` on your machine (never commit `.env`):

```dotenv
RAG_RETRIEVAL_MODE=baseline
```

Allowed modes: `baseline` (default), `multi_query`. Switch to `multi_query`
only after confirming regression tests and live chatbot behavior.

## Design decisions

- Original query is always included with weight 2.0; expansions have weight 1.0.
- Identical chunks are deduplicated by `(source, chunk_index)`.
- RRF ranks candidates and is **not** a cosine similarity. `score` is always
  similarity to the **original** question, used by existing Streamlit and
  `RAG_MIN_SIMILARITY` logic.
- Third-party credential requests matching a small deterministic pattern are
  refused in experimental mode without query expansion. **This is not a
  general-purpose security or authorization system.**
- Invalid/missing generated queries or Gemini failure fallback to baseline.
- Expansion suggestions are checked for obvious role, country, and law drift.
  These checks **cannot guarantee semantic equivalence**.
- Each multi-query request adds a Gemini interaction plus additional vector
  searches and, potentially, additional document embedding calls.

## Run tests and inspect behavior

```powershell
.\.venv\Scripts\python.exe -m pytest -q

docker compose up -d --build

docker compose exec -T api python -m pytest -q
```

With `RAG_RETRIEVAL_MODE=multi_query` set in `.env`, recreate the API container
using `docker compose up -d --force-recreate` and manually review H11-H15 and
N01-N03 via Streamlit. Compare final answers and refusal behavior against the
baseline. Test additional unseen questions before claiming improvement.

To rollback:

```dotenv
RAG_RETRIEVAL_MODE=baseline
```

Then run `docker compose up -d --force-recreate` again.

This prototype does not implement authentication, per-user document access, a
semantic entailment checker, reliable out-of-scope classification, or production
rate limiting. Keep it local with sample documents only.
