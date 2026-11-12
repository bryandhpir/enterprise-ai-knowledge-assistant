# Manual Answer-Quality Review — Baseline vs Multi-Query

**Project:** Enterprise AI Knowledge Assistant  
**Review date:** 2026-11-12  
**Based on:** `final_mode_comparison.json` (recorded run 2026-11-12 09:18:57 UTC) and the sample Markdown IT knowledge base  
**Scope:** 12 curated questions per mode (8 answerable, 4 unanswerable); `top_k=3`, V2 ChromaDB, no configured similarity threshold

> This is a qualitative review of saved model responses and the corresponding source documents. It is **not** an independent/blinded benchmark or proof of production accuracy. The reviewer did not rerun Gemini or the embedding model.

## 1. Automated metrics from the recorded run

| Metric | Baseline | Multi-Query |
| --- | ---: | ---: |
| Source hit rate — expected **file** retrieved (8 cases) | 8/8 (100.0%) | 8/8 (100.0%) |
| Valid citation ID rate (8 cases) | 5/8 (62.5%) | 7/8 (87.5%) |
| Exact no-answer refusal rate (4 cases) | 4/4 (100.0%) | 4/4 (100.0%) |
| Errors | 0 | 0 |
| Mean latency across **all 12** cases | 3.698 s | 8.706 s |

Mean latency was ~2.35× higher for Multi-Query (+5.008 s). The Multi-Query result for U02 took 0.000 s (rounded), since the request was locally rejected without generation; hence average times compare different execution paths. Case A06 in Multi-Query took 31.332 s. Repeat measurements before claiming typical or tail latency.

**Key measurement limitation:** A source hit matches a filename; it does not establish whether the *specific retrieved passage* answers the question. Similarly, a syntactically valid citation ID does not establish that the cited text supports a claim.

## 2. Manual completeness review

Ratings: **Complete** = addresses core request and necessary documented steps; **Partial** = useful but omits material guidance or introduces a caveat; **Inadequate** = refuses an answerable question, materially misleads, or fails to answer.

| ID | Request focus | Baseline | Multi-Query | Main observation |
| --- | --- | --- | --- | --- |
| A01 | Connected VPN, cannot use accounting app | **Inadequate** | **Inadequate** | Both incorrectly refuse; the precise answer is in `vpn_access.md` FAQ (chunk 22) but was not retrieved. |
| A02 | Personal laptop for remote company access | Partial | Partial | Correct rule about corporate policy and secure device; omits explicit remote access approval and other prerequisites. |
| A03 | Lost phone/MFA device; reset blocked | **Inadequate** | Partial | Multi-Query cites general IT recovery but omits *identity verification*, replacement MFA, and *do not bypass MFA*. |
| A04 | Email requests old password after reset | **Complete** | **Complete** | Both give the official restart/sign-in and IT ticket instructions. |
| A05 | Outlook not syncing despite working webmail | **Complete** | Partial | Baseline includes application version and OS for the IT ticket; Multi-Query says only to send information. |
| A06 | Urgent suspicious verification email | **Complete** | Partial | Both say avoid links and report. Multi-Query adds a possibly misleading urgent-reporting rationale: the cited criterion refers to phishing reaching *multiple* employees. |
| A07 | IT pre-handover laptop inspection | **Inadequate** | **Inadequate** | Multi-Query misleadingly says the documents cover only employee checks; the actual IT checklist exists in `device_setup.md` (chunk 16). |
| A08 | Accidentally emailed customer file outside company | **Complete** | **Complete** | Both correctly advise against silently deleting the email and urge reporting to Security/IT. |

**Human-judged completeness distribution (8 answerable cases each):**

| Classification | Baseline | Multi-Query |
| --- | ---: | ---: |
| Complete | 4/8 | 2/8 |
| Partial | 1/8 | 4/8 |
| Inadequate | 3/8 | 2/8 |

These are subjective categorical judgments for this specific saved output, **not** population-level quality estimates. Multi-Query produced fewer completely failed answers, but it did not produce more fully adequate answers on this run.

## 3. Evidence and failure mechanism

### A01 — Filename hit conceals a passage-level miss

Both modes returned `vpn_access.md` chunks 6, 4 and 3, dealing mostly with connection prerequisites/steps, then responded with the configured insufficient-information message. Yet `sample_docs/vpn_access.md`, *section 8*, contains the exact FAQ about VPN being connected but an accounting application remaining inaccessible: VPN does not grant app-level permission; the user should request an IT access check (**chunk 22**).

**Diagnosis:** Relevant document present, *relevant passage not retrieved*. This is not solved merely by checking a source filename or adding a citation ID.

### A03 — Multi-Query improves coverage but misses the critical MFA procedure

The baseline rejected the answerable query. Multi-Query used `password_reset.md` chunks 17, 13 and 10 and discussed administrative recovery; chunk 13 supports the ticket/recovery information. However, the most pertinent **chunks 14–15** instruct users who lost their MFA device **not to bypass MFA** and **to contact IT for identity verification and re-enrollment**. The answer also mentioned unusual sign-in activity, which was not called for by the user.

**Diagnosis:** Document-level success and valid source IDs, but inadequate *passage selection* for the central constraint.

### A05 — Citation-format robustness

Both modes used grouped citations such as `[S1, S2]`, while the existing citation checker primarily recognizes individual tokens like `[S1]` via a regex. A response can therefore pass overall ID validation because it contains other valid tokens even though grouped citations are not individually verified. This is a parser/validation limitation; do not treat Valid Citation ID Rate as claim-level evidence verification.

### A07 — Incorrect assertion despite a valid citation ID

Baseline returned the citation-validation fallback. Multi-Query stated that the documentation only covered new employee steps and cited `device_setup.md` chunk 20. This passage indeed covers the employee's first-day checklist, but **section 3, step 5** of the same document separately lists the IT team's pre-handover checks: successful login, required applications, MFA/VPN where authorized, device encryption/update/security compliance, etc. (notably **chunk 16**). Section 3, step 6 provides handover/asset-record details (chunk 18).

**Diagnosis:** A valid reference ID is present, but the answer's broad claim that guidance is unavailable is wrong.

### A06 — Avoid overclaiming urgency

Multi-Query correctly provides phishing guidance, then adds that the event may warrant urgent reporting on the authority of an IT Helpdesk passage about **phishing sent to multiple employees**. The provided question concerns one suspicious email and does not establish this criterion. The response should not conflate normal reporting with that specific bulk-incident escalation condition.

## 4. Unanswerable cases

U01–U04 all returned the configured no-evidence response in both modes (4/4 each). This is a useful result, but only on the four selected queries. U02 was short-circuited in Multi-Query with no sources, no model, and a rounded 0.000-second elapsed time.

Neither test establishes authorization, tenant isolation, or secret exfiltration resistance in a real corporate environment.

## 5. Engineering recommendation and priorities

**Keep `RAG_RETRIEVAL_MODE=baseline` as the default for now; retain `multi_query` as an opt-in experimental strategy.** Multi-Query helped with the earlier paraphrased H12 problem and avoided one baseline no-answer case (A03), but the new report exposes passage-selection failures in both modes, a material latency cost, and incomplete/manual-evidence coverage.

Suggested next improvements, in order:

1. **Passage-level retrieval evaluation.** Add expected `source + chunk_index` or passage IDs to the test set (rather than only document names), with examples A01→`vpn_access.md#22`, A03→`password_reset.md#14/15`, A07→`device_setup.md#16/18`. Include annotations for relevance, not just exact matching.
2. **Candidate expansion + reranking.** Retrieve more than three *candidate passages*, rerank against the original question, and only then send the final Top-3 to Gemini; measure whether the relevant FAQ/checklists enter context. Compare against the existing mode without overwriting baseline.
3. **Context-aware coverage check.** Before generating, detect when the question asks for a specific procedure but the retrieved evidence only contains generic information; either retrieve additional passage candidates or transparently state uncertainty, without asserting that no such documentation exists.
4. **Citation parser and source attribution.** Handle citation groups, reject truly invalid IDs, and compare each material claim to its cited passage via human review before calling citations “supported.”
5. **Repeat & broaden evaluation.** Run multiple seeds/requests with preserved query variants, assess intent drift, use fresh questions and new documents, and report median/P95 latency as well as means. Keep evaluation artifacts containing generated outputs separate from code/configuration.
6. **End-to-end regression.** Test answering, calibrated refusal, safety boundaries, and source quality across modes; verify Docker and GitHub Actions again before merging.

## 6. Reporting / interpretation cautions

- The archived dataset is **curated after earlier diagnostic work**, not an untouched holdout.
- The `manual_review` status in the original report was `not_assessed`; a separate annotated JSON is provided so that the original remains unchanged.
- The content here compares **one saved run** of each mode; Gemini generations and paraphrases are nondeterministic.
- Source passages were checked against the current repository's sample Markdown documents and source-chunking logic, not a direct export of the particular stored ChromaDB collection.
- The corpus is **fictional sample IT policy**, not actual company guidance; there is no live identity/access management or verified organizational authorization.

**Recommended placement:** `docs/MANUAL_ANSWER_REVIEW.md`  
**Annotated per-case data:** `evals/reports/final_mode_comparison_reviewed.json`
