# End-to-End RAG Mode Comparison

Generated UTC: 2026-11-12T11:18:17.136604+00:00
Dataset: `/app/evals/final_eval_questions.json` (12 of 12 cases)
Retrieval collection: `it_knowledge_base_v2`; Top-K: 3
Similarity threshold: `disabled`

> This is an additional curated challenge set. It is not an independent or blinded holdout.
> Model generation can vary between runs. Neighboring chunks are deterministic.

## Automated metrics

| Metric | rerank_original | rerank_with_neighbors |
| --- | ---: | ---: |
| Source Hit Rate (answerable) | 100.0% | 100.0% |
| Valid Citation ID Rate (answerable) | 100.0% | 100.0% |
| Correct Refusal Rate (unanswerable) | 75.0% | 100.0% |
| Average latency (seconds; all cases) | 7.526 | 10.727 |
| Errors | 0 | 0 |

## Per-case results

| Case | Mode | Source Hit | Citation IDs | Refusal | Latency (s) | Error |
| --- | --- | --- | --- | --- | ---: | --- |
| A01 | rerank_original | Pass | Pass | N/A | 6.884 | - |
| A01 | rerank_with_neighbors | Pass | Pass | N/A | 75.308 | - |
| A02 | rerank_original | Pass | Pass | N/A | 12.558 | - |
| A02 | rerank_with_neighbors | Pass | Pass | N/A | 4.148 | - |
| A03 | rerank_original | Pass | Pass | N/A | 3.816 | - |
| A03 | rerank_with_neighbors | Pass | Pass | N/A | 3.774 | - |
| A04 | rerank_original | Pass | Pass | N/A | 4.654 | - |
| A04 | rerank_with_neighbors | Pass | Pass | N/A | 4.963 | - |
| A05 | rerank_original | Pass | Pass | N/A | 12.471 | - |
| A05 | rerank_with_neighbors | Pass | Pass | N/A | 4.011 | - |
| A06 | rerank_original | Pass | Pass | N/A | 12.721 | - |
| A06 | rerank_with_neighbors | Pass | Pass | N/A | 4.982 | - |
| A07 | rerank_original | Pass | Pass | N/A | 12.811 | - |
| A07 | rerank_with_neighbors | Pass | Pass | N/A | 8.024 | - |
| A08 | rerank_original | Pass | Pass | N/A | 3.987 | - |
| A08 | rerank_with_neighbors | Pass | Pass | N/A | 3.567 | - |
| U01 | rerank_original | N/A | N/A | Pass | 3.954 | - |
| U01 | rerank_with_neighbors | N/A | N/A | Pass | 8.619 | - |
| U02 | rerank_original | N/A | N/A | Fail | 3.556 | - |
| U02 | rerank_with_neighbors | N/A | N/A | Pass | 3.925 | - |
| U03 | rerank_original | N/A | N/A | Pass | 8.319 | - |
| U03 | rerank_with_neighbors | N/A | N/A | Pass | 3.777 | - |
| U04 | rerank_original | N/A | N/A | Pass | 4.583 | - |
| U04 | rerank_with_neighbors | N/A | N/A | Pass | 3.628 | - |

## Manual answer review — not yet performed

Inspect each generated answer against the relevant document passage, then fill in the JSON
`manual_review` fields. The `review_focus` field provides a starting point, not an automated verdict.

| Case | Mode | Grounded | Complete | Claim citations supported |
| --- | --- | --- | --- | --- |
| A01 | rerank_original | Not assessed | Not assessed | Not assessed |
| A01 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A02 | rerank_original | Not assessed | Not assessed | Not assessed |
| A02 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A03 | rerank_original | Not assessed | Not assessed | Not assessed |
| A03 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A04 | rerank_original | Not assessed | Not assessed | Not assessed |
| A04 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A05 | rerank_original | Not assessed | Not assessed | Not assessed |
| A05 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A06 | rerank_original | Not assessed | Not assessed | Not assessed |
| A06 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A07 | rerank_original | Not assessed | Not assessed | Not assessed |
| A07 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| A08 | rerank_original | Not assessed | Not assessed | Not assessed |
| A08 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| U01 | rerank_original | Not assessed | Not assessed | Not assessed |
| U01 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| U02 | rerank_original | Not assessed | Not assessed | Not assessed |
| U02 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| U03 | rerank_original | Not assessed | Not assessed | Not assessed |
| U03 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |
| U04 | rerank_original | Not assessed | Not assessed | Not assessed |
| U04 | rerank_with_neighbors | Not assessed | Not assessed | Not assessed |

## Interpretation limits

- Source Hit uses filenames, not passage-level relevance.
- A valid citation ID is not proof that a statement is supported.
- The correct-refusal metric checks an exact configured no-answer response.
- Failure rows count as unsuccessful for success-rate denominators.
- The saved JSON includes generated answers and returned source metadata for manual inspection.
- This run does not cache generated variants or assess whether query rewrites preserved intent.
- Neither result establishes production reliability, authorization, or protection of private data.
