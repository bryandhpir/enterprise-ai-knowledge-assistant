# RAG Evaluation Report

**Project:** Enterprise AI Knowledge Assistant  
**Recorded run (UTC):** 2026-11-10 00:12:58  
**Collection:** `it_knowledge_base_v2`  
**Top-K:** 3  
**Minimum similarity threshold:** disabled (empty configuration)  
**Dataset:** 8 examples — 5 labeled answerable, 3 labeled unanswerable

> This report summarizes **actual saved results** from `evals/reports/rag_eval.json` on the repository's default branch. It is not a new measurement, and manual grounding review is not yet complete.

## Automated results

| Metric | Numerator / denominator | Recorded result |
| --- | ---: | ---: |
| Source Hit Rate (answerable cases) | 4 / 5 | **80.0%** |
| Citation ID Valid Rate (answerable cases) | 4 / 5 | **80.0%** |
| Correct Refusal Rate (unanswerable cases) | 3 / 3 | **100.0%** |

**Metric definitions:** Source Hit means an expected source filename appeared among the retrieved passages. Citation ID Valid checks whether the generated answer cites existing IDs such as `[S1]`; it does not test whether the cited chunk entails a claim. Correct Refusal checks whether the answer equals the designated no-answer text for labeled unanswerable questions.

## Per-question outcomes

| ID | Subject | Expected source | Source hit | Citation IDs | Correct refusal |
| --- | --- | --- | --- | --- | --- |
| H11 | Locked company account | `password_reset.md` | Pass | Pass | N/A |
| H12 | Accessing internal resources away from office | `vpn_access.md` | **Fail** | **Fail** | N/A |
| H13 | Email app problems | `email_support.md` | Pass | Pass | N/A |
| H14 | New-employee laptop setup | `device_setup.md` | Pass | Pass | N/A |
| H15 | Information security rules | `security_policy.md` | Pass | Pass | N/A |
| N01 | Cooking a dish | None | N/A | N/A | Pass |
| N02 | Live gold pricing | None | N/A | N/A | Pass |
| N03 | An executive's VPN password | None | N/A | N/A | Pass |

## Failure analysis

### H12 — retrieval miss

The request concerned using company resources outside the office, but none of the top-three passages came from `vpn_access.md`. The retrieved sources were `device_setup.md`, `email_support.md`, and `device_setup.md` with scores approximately **0.4199**, **0.3980**, and **0.3634**. The chatbot returned a no-answer response. The relevant VPN instructions **do exist** in the corpus, so this is a retrieval-coverage failure rather than a genuinely unanswerable question.

**Candidate investigations:** Query paraphrases, additional document context, hybrid keyword+dense retrieval, reranking, and passage-level relevance labels. These are investigation directions, not implemented fixes.

### H11 — source hit does not guarantee completeness

The expected `password_reset.md` appeared in the retrieved sources and citation IDs were valid. However, the response began by stating that it lacked enough information to specify the contact. The original document includes instructions to contact the official IT Helpdesk when self-service password reset fails. The answer therefore needs manual review for coverage and phrasing even though the automated source/citation indicators passed.

### N03 — similarity is not answerability

A question asking for a specific individual's VPN password returned an appropriate no-answer response, despite one retrieved passage having a similarity score around **0.7246**. A high semantic match cannot justify supplying credentials or inventing facts.

## Manual answer-quality review

The automated evaluator does **not** score full groundedness, completeness, or claim-level citation support. These items remain **not assessed** until someone checks each answer against the saved `evidence` chunks in `rag_eval.json`.

| ID | Groundedness | Completeness | Claim-level citation support | Reviewer notes |
| --- | --- | --- | --- | --- |
| H11 | Not assessed | Not assessed | Not assessed | Inspect omitted Helpdesk contact guidance |
| H12 | Not assessed | Not assessed | Not assessed | Retrieval missed VPN guide |
| H13 | Not assessed | Not assessed | Not assessed | |
| H14 | Not assessed | Not assessed | Not assessed | |
| H15 | Not assessed | Not assessed | Not assessed | |
| N01 | N/A | N/A | N/A | Check refusal behavior |
| N02 | N/A | N/A | N/A | Check refusal behavior |
| N03 | N/A | N/A | N/A | Check refusal behavior |

## Interpretation and reproducibility

- This dataset is **small**. The 100% refusal rate comes from only three examples.
- Several answerable cases originate from questions used in prior retrieval comparisons; the sample is not a pristine unseen benchmark.
- Metrics are reported as measured, not as claimed production accuracy.
- Generation can vary by request and model version; rerunning the dataset may produce different results.
- Keep `.env` and real enterprise secrets out of the repository and evaluation artifacts.

Run the full evaluation from the repository root:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_rag
```

For a smoke test, a limited run should use a separate preview filename so it does not overwrite this full-run report. The accompanying revised evaluation runner implements that behavior.
