# End-to-End RAG Mode Comparison

Generated UTC: 2026-11-12T10:52:55.841944+00:00
Dataset: `/app/evals/final_eval_questions.json` (12 of 12 cases)
Retrieval collection: `it_knowledge_base_v2`; Top-K: 3
Similarity threshold: `disabled`

> This is an additional curated challenge set. It is not an independent or blinded holdout.
> Model generation and query expansion can vary between runs.

## Automated metrics

| Metric | baseline | rerank |
| --- | ---: | ---: |
| Source Hit Rate (answerable) | 100.0% | 100.0% |
| Valid Citation ID Rate (answerable) | 62.5% | 100.0% |
| Correct Refusal Rate (unanswerable) | 100.0% | 100.0% |
| Average latency (seconds; all cases) | 5.749 | 4.143 |
| Errors | 0 | 0 |

## Per-case results

| Case | Mode | Source Hit | Citation IDs | Refusal | Latency (s) | Error |
| --- | --- | --- | --- | --- | ---: | --- |
| A01 | baseline | Pass | Fail | N/A | 6.627 | - |
| A01 | rerank | Pass | Pass | N/A | 3.958 | - |
| A02 | baseline | Pass | Pass | N/A | 4.077 | - |
| A02 | rerank | Pass | Pass | N/A | 3.466 | - |
| A03 | baseline | Pass | Fail | N/A | 8.095 | - |
| A03 | rerank | Pass | Pass | N/A | 3.519 | - |
| A04 | baseline | Pass | Pass | N/A | 3.597 | - |
| A04 | rerank | Pass | Pass | N/A | 3.854 | - |
| A05 | baseline | Pass | Pass | N/A | 9.666 | - |
| A05 | rerank | Pass | Pass | N/A | 9.316 | - |
| A06 | baseline | Pass | Pass | N/A | 6.511 | - |
| A06 | rerank | Pass | Pass | N/A | 3.705 | - |
| A07 | baseline | Pass | Fail | N/A | 3.906 | - |
| A07 | rerank | Pass | Pass | N/A | 4.414 | - |
| A08 | baseline | Pass | Pass | N/A | 4.130 | - |
| A08 | rerank | Pass | Pass | N/A | 3.279 | - |
| U01 | baseline | N/A | N/A | Pass | 3.344 | - |
| U01 | rerank | N/A | N/A | Pass | 3.182 | - |
| U02 | baseline | N/A | N/A | Pass | 4.639 | - |
| U02 | rerank | N/A | N/A | Pass | 3.556 | - |
| U03 | baseline | N/A | N/A | Pass | 5.815 | - |
| U03 | rerank | N/A | N/A | Pass | 3.800 | - |
| U04 | baseline | N/A | N/A | Pass | 8.584 | - |
| U04 | rerank | N/A | N/A | Pass | 3.664 | - |

## Manual answer review — not yet performed

Inspect each generated answer against the relevant document passage, then fill in the JSON
`manual_review` fields. The `review_focus` field provides a starting point, not an automated verdict.

| Case | Mode | Grounded | Complete | Claim citations supported |
| --- | --- | --- | --- | --- |
| A01 | baseline | Not assessed | Not assessed | Not assessed |
| A01 | rerank | Not assessed | Not assessed | Not assessed |
| A02 | baseline | Not assessed | Not assessed | Not assessed |
| A02 | rerank | Not assessed | Not assessed | Not assessed |
| A03 | baseline | Not assessed | Not assessed | Not assessed |
| A03 | rerank | Not assessed | Not assessed | Not assessed |
| A04 | baseline | Not assessed | Not assessed | Not assessed |
| A04 | rerank | Not assessed | Not assessed | Not assessed |
| A05 | baseline | Not assessed | Not assessed | Not assessed |
| A05 | rerank | Not assessed | Not assessed | Not assessed |
| A06 | baseline | Not assessed | Not assessed | Not assessed |
| A06 | rerank | Not assessed | Not assessed | Not assessed |
| A07 | baseline | Not assessed | Not assessed | Not assessed |
| A07 | rerank | Not assessed | Not assessed | Not assessed |
| A08 | baseline | Not assessed | Not assessed | Not assessed |
| A08 | rerank | Not assessed | Not assessed | Not assessed |
| U01 | baseline | Not assessed | Not assessed | Not assessed |
| U01 | rerank | Not assessed | Not assessed | Not assessed |
| U02 | baseline | Not assessed | Not assessed | Not assessed |
| U02 | rerank | Not assessed | Not assessed | Not assessed |
| U03 | baseline | Not assessed | Not assessed | Not assessed |
| U03 | rerank | Not assessed | Not assessed | Not assessed |
| U04 | baseline | Not assessed | Not assessed | Not assessed |
| U04 | rerank | Not assessed | Not assessed | Not assessed |

## Interpretation limits

- Source Hit uses filenames, not passage-level relevance.
- A valid citation ID is not proof that a statement is supported.
- The correct-refusal metric checks an exact configured no-answer response.
- Failure rows count as unsuccessful for success-rate denominators.
- The saved JSON includes generated answers and returned source metadata for manual inspection.
- This run does not cache generated variants or assess whether query rewrites preserved intent.
- Neither result establishes production reliability, authorization, or protection of private data.
