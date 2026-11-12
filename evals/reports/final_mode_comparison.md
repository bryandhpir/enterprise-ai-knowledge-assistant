# End-to-End RAG Mode Comparison

Generated UTC: 2026-11-12T09:18:57.572909+00:00
Dataset: `/app/evals/final_eval_questions.json` (12 of 12 cases)
Retrieval collection: `it_knowledge_base_v2`; Top-K: 3
Similarity threshold: `disabled`

> This is an additional curated challenge set. It is not an independent or blinded holdout.
> Model generation and query expansion can vary between runs.

## Automated metrics

| Metric | baseline | multi_query |
| --- | ---: | ---: |
| Source Hit Rate (answerable) | 100.0% | 100.0% |
| Valid Citation ID Rate (answerable) | 62.5% | 87.5% |
| Correct Refusal Rate (unanswerable) | 100.0% | 100.0% |
| Average latency (seconds; all cases) | 3.698 | 8.706 |
| Errors | 0 | 0 |

## Per-case results

| Case | Mode | Source Hit | Citation IDs | Refusal | Latency (s) | Error |
| --- | --- | --- | --- | --- | ---: | --- |
| A01 | baseline | Pass | Fail | N/A | 6.298 | - |
| A01 | multi_query | Pass | Fail | N/A | 8.072 | - |
| A02 | baseline | Pass | Pass | N/A | 3.343 | - |
| A02 | multi_query | Pass | Pass | N/A | 6.667 | - |
| A03 | baseline | Pass | Fail | N/A | 3.182 | - |
| A03 | multi_query | Pass | Pass | N/A | 7.992 | - |
| A04 | baseline | Pass | Pass | N/A | 4.256 | - |
| A04 | multi_query | Pass | Pass | N/A | 7.676 | - |
| A05 | baseline | Pass | Pass | N/A | 3.880 | - |
| A05 | multi_query | Pass | Pass | N/A | 7.443 | - |
| A06 | baseline | Pass | Pass | N/A | 3.640 | - |
| A06 | multi_query | Pass | Pass | N/A | 31.332 | - |
| A07 | baseline | Pass | Fail | N/A | 2.795 | - |
| A07 | multi_query | Pass | Pass | N/A | 7.068 | - |
| A08 | baseline | Pass | Pass | N/A | 3.293 | - |
| A08 | multi_query | Pass | Pass | N/A | 6.606 | - |
| U01 | baseline | N/A | N/A | Pass | 3.659 | - |
| U01 | multi_query | N/A | N/A | Pass | 6.571 | - |
| U02 | baseline | N/A | N/A | Pass | 3.581 | - |
| U02 | multi_query | N/A | N/A | Pass | 0.000 | - |
| U03 | baseline | N/A | N/A | Pass | 3.603 | - |
| U03 | multi_query | N/A | N/A | Pass | 7.694 | - |
| U04 | baseline | N/A | N/A | Pass | 2.843 | - |
| U04 | multi_query | N/A | N/A | Pass | 7.353 | - |

## Manual answer review — not yet performed

Inspect each generated answer against the relevant document passage, then fill in the JSON
`manual_review` fields. The `review_focus` field provides a starting point, not an automated verdict.

| Case | Mode | Grounded | Complete | Claim citations supported |
| --- | --- | --- | --- | --- |
| A01 | baseline | Not assessed | Not assessed | Not assessed |
| A01 | multi_query | Not assessed | Not assessed | Not assessed |
| A02 | baseline | Not assessed | Not assessed | Not assessed |
| A02 | multi_query | Not assessed | Not assessed | Not assessed |
| A03 | baseline | Not assessed | Not assessed | Not assessed |
| A03 | multi_query | Not assessed | Not assessed | Not assessed |
| A04 | baseline | Not assessed | Not assessed | Not assessed |
| A04 | multi_query | Not assessed | Not assessed | Not assessed |
| A05 | baseline | Not assessed | Not assessed | Not assessed |
| A05 | multi_query | Not assessed | Not assessed | Not assessed |
| A06 | baseline | Not assessed | Not assessed | Not assessed |
| A06 | multi_query | Not assessed | Not assessed | Not assessed |
| A07 | baseline | Not assessed | Not assessed | Not assessed |
| A07 | multi_query | Not assessed | Not assessed | Not assessed |
| A08 | baseline | Not assessed | Not assessed | Not assessed |
| A08 | multi_query | Not assessed | Not assessed | Not assessed |
| U01 | baseline | Not assessed | Not assessed | Not assessed |
| U01 | multi_query | Not assessed | Not assessed | Not assessed |
| U02 | baseline | Not assessed | Not assessed | Not assessed |
| U02 | multi_query | Not assessed | Not assessed | Not assessed |
| U03 | baseline | Not assessed | Not assessed | Not assessed |
| U03 | multi_query | Not assessed | Not assessed | Not assessed |
| U04 | baseline | Not assessed | Not assessed | Not assessed |
| U04 | multi_query | Not assessed | Not assessed | Not assessed |

## Interpretation limits

- Source Hit uses filenames, not passage-level relevance.
- A valid citation ID is not proof that a statement is supported.
- The correct-refusal metric checks an exact configured no-answer response.
- Failure rows count as unsuccessful for success-rate denominators.
- The saved JSON includes generated answers and returned source metadata for manual inspection.
- This run does not cache generated variants or assess whether query rewrites preserved intent.
- Neither result establishes production reliability, authorization, or protection of private data.
