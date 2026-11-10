# Week 4 — RAG Evaluation Report

Generated (UTC): 2026-11-10T00:12:58.226287+00:00
Collection: it_knowledge_base_v2
Top-K: 3
Evaluated questions: 8

## Automated Metrics

- source_hit_rate: 80.0%
- citation_id_valid_rate: 80.0%
- unanswerable_refusal_rate: 100.0%

## Per-question Results

| ID | Source Hit | Citation IDs | Correct Refusal |
| --- | --- | --- | --- |
| H11 | Pass | Pass | N/A |
| H12 | Fail | Fail | N/A |
| H13 | Pass | Pass | N/A |
| H14 | Pass | Pass | N/A |
| H15 | Pass | Pass | N/A |
| N01 | N/A | N/A | Pass |
| N02 | N/A | N/A | Pass |
| N03 | N/A | N/A | Pass |

## Manual Review

Review each answer against its exact retrieved chunks.
Use the evidence stored in week4_rag_eval.json.

| ID | Grounded 0/1 | Complete 0/1 | Citation supported 0/1 | Notes |
| --- | --- | --- | --- | --- |
| H11 | TBD | TBD | TBD | |
| H12 | TBD | TBD | TBD | |
| H13 | TBD | TBD | TBD | |
| H14 | TBD | TBD | TBD | |
| H15 | TBD | TBD | TBD | |
| N01 | TBD | TBD | TBD | |
| N02 | TBD | TBD | TBD | |
| N03 | TBD | TBD | TBD | |

## Limitations

- Source Hit measures source-level retrieval only.
- Citation ID validation does not prove claim support.
- Groundedness and completeness require manual review.
- Generation can vary between runs.
- The five historical holdout questions have been used in prior analysis.
