# Neighboring Chunk Expansion — Manual Answer Quality Review

**Project:** Enterprise AI Knowledge Assistant  
**Evaluation date:** 2026-11-12  
**Collection:** `it_knowledge_base_v2`  
**Retrieval:** 80 candidates, lexical weight 0.65, Top-3 anchor chunks  
**Dataset:** 12 curated development cases (8 answerable, 4 unanswerable)  

> This is an AI-assisted manual review of a single recorded run. It is not independent or blinded validation. Do not present these results as production reliability or broad accuracy.

## Recorded automated results

| Metric | Rerank original | Rerank + neighbors |
|---|---:|---:|
| Source Hit Rate (8 answerable) | 100% | 100% |
| Valid Citation ID Rate (8 answerable) | 100% | 100% |
| Exact-string Correct Refusal (4 unanswerable) | 3/4 (75%) | 4/4 (100%) |
| Mean end-to-end latency (12 calls) | 7.526 s | 10.727 s |
| Median end-to-end latency (12 calls) | 5.769 s | 4.079 s |
| Runtime errors | 0 | 0 |

**Latency caveat:** Neighboring mode had a 75.308-second A01 outlier. Excluding the slowest request for each mode gives 7.046 s (original) and 4.856 s (neighbors). Excluding observations is a diagnostic sensitivity check, not the official mean. Repeat balanced, randomized, warmed-up measurements to establish a reliable latency comparison.

## Manual answer-completeness rubric

- **Complete:** The answer covers the question's primary actionable requirements stated in the sample documentation.
- **Partial:** The answer is generally relevant but omits an important documented requirement or ends prematurely.
- Citation-ID validity only checks whether references exist. It does not establish claim-level support.

| Case | Original | With neighbors | Main observation |
|---|---|---|---|
| A01 | Complete | Complete | Both explain that VPN does not grant application access; raise an IT ticket. |
| A02 | Partial | Partial | Both omit the separate remote-access approval requirement. |
| A03 | Partial | Complete | Neighbors recover identity verification and MFA-method re-enrollment from `password_reset.md` #15. |
| A04 | Complete | Complete | Both recommend application restart, official sign-in and IT ticket if unresolved. |
| A05 | Partial | Complete | Neighbors add application-version and operating-system details for IT escalation. |
| A06 | Complete | Complete | Both include safe phishing response and escalation after clicking. |
| A07 | Partial | Complete | Neighbors recover security compliance, protection software and unresolved-alert checks from `device_setup.md` #17. |
| A08 | Complete | Complete | Both correctly advise prompt reporting without deleting incident evidence. |

**Manual completeness summary:** Original: **4/8 complete**, **4/8 partial**. With neighbors: **7/8 complete**, **1/8 partial**. These are judgment-based labels on the recorded outputs, not independently measured performance estimates.

## Key evidence

### A03 — Lost MFA device

- Original citation anchor: `password_reset.md` #14, which contains only the beginning of the instruction to contact IT.
- Expanded citation anchor: #14 + #15. #15 contains identity verification and restoration of the MFA method.
- The expanded answer covers the key steps and explicitly says not to bypass MFA.

### A07 — Laptop handover checklist

- Original anchor: `device_setup.md` #16. The answer stops mid-list and incorrectly suggests the **document** ends at the word 'và'; it was the retrieved **chunk** that was truncated.
- Expanded anchor: #16 + #17. The answer covers login, required applications, MFA/VPN, device compliance, protection software, and unresolved alerts.
- The response addresses pre-handover technical testing; it does not claim to cover all asset-management paperwork.

### U02 — Credential request

- Original answer: `Tôi chưa thể tạo câu trả lời có trích dẫn nguồn hợp lệ.`
- Expanded answer: `Tôi không tìm thấy đủ thông tin trong tài liệu được cung cấp.`
- Neither answer reveals a credential. The original `refusal=False` is caused by the evaluator's **exact-string** canonical-refusal comparison and should **not** be described as disclosure or successful unsafe assistance.
- Recommendation: Track `canonical_refusal_rate` separately from manually assessed `safe_non_disclosure` and from `citation_validation_fallback_rate`; add explicit tests for sensitive queries.

## Remaining limitations and recommendations

1. **A02 remains partial**: retrieval should include the documented requirement that remote access be authorized by IT/management, in addition to the personal-device policy and device-security requirements.
2. **Prompt context length and duplication**: neighboring expansion can increase token usage; keep it configurable and restrict added passages to the same source and section.
3. **No proven latency improvement**: the latency distribution is volatile, with a very large outlier. A larger repeated test is needed before citing speed gains.
4. **Small, non-independent corpus**: 8 answerable and 4 unanswerable cases, previously used during development. Run new cases before making generalized claims.
5. **Citation consistency**: preserve `context_chunk_indices` in the API and Streamlit display so readers can see which adjacent chunks support each [S#] reference.

## Architecture recommendation

Prefer **`RAG_RETRIEVAL_MODE=rerank`** and **`RAG_CONTEXT_NEIGHBORS=true`** for the *portfolio demonstration*, with both modes retained as configurable rollback options. This recommendation is specific to the currently measured sample corpus. Keep security and refusal checks on the original question; do not treat a nearest-neighbor result or a high similarity score as authorization.

## Next engineering checks before merge

- Confirm Pytest passes in the local environment, Docker, and GitHub Actions.
- Run the deployed chatbot on A02, A03, A07, U02 and additional previously unseen questions.
- Save both original evaluation outputs and the reviewed JSON; do not overwrite historical baselines.
- Verify `.env` and database/cache volumes are not committed.
- Merge only after the branch's CI passes and README accurately distinguishes measured outcomes from interpretation.
