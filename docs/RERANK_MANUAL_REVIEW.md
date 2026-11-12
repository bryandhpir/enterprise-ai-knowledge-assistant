# Reranking — Manual Answer Quality Review

**Project:** Enterprise AI Knowledge Assistant  
**Recorded evaluation:** 2026-11-12, `rerank_e2e_comparison.json`  
**Corpus:** Five fictional enterprise IT Markdown guides  
**Collection:** `it_knowledge_base_v2`; `top_k=3`  
**Rerank settings:** 80 dense candidates; lexical weight 0.65  
**Dataset:** 12 curated development questions (8 answerable, 4 unanswerable)

> **Scope and limitations:** These results reflect one saved run on a small, non-blinded development set used during method selection. They must not be represented as independent test performance or production reliability. This review cross-checks saved generated answers and cited passage IDs against the current sample documentation. It does **not** rerun Gemini.

## Automated results (recorded)

| Metric | Baseline | Rerank |
| --- | ---: | ---: |
| Source Hit Rate, 8 answerable cases | 8/8 (100%) | 8/8 (100%) |
| Valid Citation ID Rate, 8 answerable cases | 5/8 (62.5%) | 8/8 (100%) |
| Exact Correct Refusal Rate, 4 unanswerable cases | 4/4 (100%) | 4/4 (100%) |
| Mean response latency across 12 cases | 5.749 seconds | 4.143 seconds |
| Execution errors | 0 | 0 |

The observed latency difference is 1.606 seconds per case (approximately 27.9%) **in this run only**. Baseline and rerank were not independently randomized or repeatedly benchmarked, so a general speed advantage is not established. Valid citation IDs are not a measure of factual entailment.

## Human-readable answer-quality verdicts

Rubric: **Complete** = the saved answer covers the core actionable points in the relevant document, with support from cited passages; **Partial** = directionally correct but omits material guidance; **Not answered** = incorrect insufficient-information fallback despite an answer being present. These are judgment calls about *this saved response*, not estimated population-level accuracy.

| Case | Baseline | Rerank | Rerank observations |
| --- | --- | --- | --- |
| A01 — VPN connected, accounting app inaccessible | Not answered | **Complete** | Correctly explains VPN does not grant app access, and directs user to IT to review permissions; cites `vpn_access.md#22`. |
| A02 — Personal laptop for remote access | Partial | Partial | States device must be allowed by company policy and meet security requirements, but omits remote-access approval by management/IT. |
| A03 — Lost MFA phone | Not answered | Partial | Correctly advises not bypassing MFA and contacting IT, but omits verified identity recovery and MFA re-enrollment. `password_reset.md#15` holds the fuller continuation. |
| A04 — Email requests old password | **Complete** | **Complete** | Restart and sign in using official flow; open a Helpdesk ticket if needed. |
| A05 — Outlook not syncing with webmail | **Complete** | Partial | Core troubleshooting correct, but rerank answer omits sending application version and OS details to IT. |
| A06 — Urgent suspicious verification email | **Complete** | **Complete** | Avoid link, verify through official channels, report potential phishing; rerank also mentions notifying IT if already interacted with the link. |
| A07 — IT pre-handover device checklist | Not answered | Partial | Retrieves `device_setup.md#16`; covers login, apps, MFA/VPN, encryption/update, but misses endpoint compliance/protection checks in chunk 17 and asset/handover records. |
| A08 — Mis-sent customer data | **Complete** | **Complete** | Correctly says not to delete and ignore the incident; report to IT/Security. |

### Totals (8 answerable questions)

| Manual verdict | Baseline | Rerank |
| --- | ---: | ---: |
| Complete | 4/8 | 4/8 |
| Partial | 1/8 | 4/8 |
| Not answered (incorrect fallback) | 3/8 | **0/8** |

**Interpretation:** Reranking substantially reduces false insufficient-information responses in this saved run: A01, A03 and A07 now receive substantive, source-grounded answers. However, the number of **complete** answers does not increase because A02, A03, A05 and A07 still omit some necessary details. It would be misleading to claim "100% answer accuracy."

### Evidence-specific caveats

- **A03:** The selected `password_reset.md#14` ends at a sentence boundary split: the next chunk (#15) specifies contacting IT for identity verification and restoration of the MFA method. The rerank answer has the right general direction but insufficient detail; the citation evidence is not complete for the full recovery process.
- **A07:** `device_setup.md#16` cuts off after 'Thiết bị mã hóa, cập nhật và'; #17 contains the remaining compliance and protective software checks. The chosen context therefore misses the tail of the checklist.
- **A05:** Baseline retrieved `email_support.md#17`, containing the application-version and operating-system details; rerank retrieved #16 but not #17. This helps explain the content regression.
- **A06:** The reranked top passage is from the password reset guide, but the answer's actual claims are supported by the cited `email_support.md#25` and `#19`. Source hit alone cannot quantify passage relevance.
- **A02:** Both answers are faithful to `vpn_access.md#23` but do not cover a separate approval requirement from the VPN prerequisites section.

### Refusal tests

U01 (live football result), U02 (another person's VPN password), U03 (private salary), and U04 (future internal notice) all returned the canonical insufficient-information message in both modes: **4/4** in this small curated set. This does not establish an exhaustive safety or authorization boundary.

## Architecture decision

**Recommend `rerank` as the preferred *local portfolio demo* retrieval mode**, with `baseline` retained as a configurable fallback and `multi_query` remaining an experiment. Reranking is a light-weight second stage and, on this development set, materially reduces false refusals without an extra query-generation LLM call.

**Do not label this production-ready.** Before a general deployment decision, assess unseen questions, more document types, additional languages, authorization rules, and repeated latency measurements.

## Most useful next improvement

Use **passage-window expansion** for rerank winners: when a top passage is returned, attach one neighboring chunk (subject to same document and heading), or select a wider coherent passage before passing evidence to Gemini. Keep source-ID mapping correct and cap the total context size.

Priority regression cases:
- A03: include `password_reset.md#15` with #14.
- A07: include `device_setup.md#17` with #16.
- A05: include `email_support.md#17` with #16.
- A01: preserve the correct answer from `vpn_access.md#22`.
- H12: preserve coverage for indirect remote-access queries.
- U01–U04: maintain appropriate refusal on unsupported questions.

**Important:** Passage-window expansion must be evaluated separately; extra context is not guaranteed to improve generated answers. Add tests ensuring adjacent chunks do not cross document boundaries or unrelated headings.

## Portfolio wording

> Implemented a multilingual enterprise IT RAG prototype with FastAPI, Streamlit, ChromaDB, Gemini, Docker Compose, and GitHub Actions CI. Evaluated baseline, multi-query retrieval, and lightweight lexical reranking. On a curated 8-question development set, passage Hit@3 improved from 62.5% to 100%. In a 12-case recorded end-to-end run, the rerank configuration improved valid citation ID rate from 62.5% to 100% and eliminated three incorrect insufficient-information responses, while manual review identified remaining answer-completeness gaps.

This paragraph intentionally does not claim independent/generalized accuracy or full claim-level verification.

---

**Source data:** [`rerank_e2e_comparison.json`](../evals/reports/rerank_e2e_comparison.json) and the annotated copy [`rerank_e2e_comparison_reviewed.json`](../evals/reports/rerank_e2e_comparison_reviewed.json). Suggested GitHub path for this document: `docs/RERANK_MANUAL_REVIEW.md`.
