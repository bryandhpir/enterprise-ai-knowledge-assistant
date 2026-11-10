# Portfolio & CV Project Description

These are ready-to-edit descriptions grounded in the implemented code and recorded evaluation. They intentionally avoid claims of production deployment or enterprise adoption.

## Project title

**Enterprise AI Knowledge Assistant — Multilingual RAG Chatbot**

**Stack:** Python · FastAPI · Sentence Transformers · ChromaDB · Google Gemini · Streamlit · Pytest

## CV — concise version (English)

**Enterprise AI Knowledge Assistant | Personal AI Engineering Project**

- Built a multilingual RAG application for sample IT-support documents using FastAPI, Sentence Transformers, ChromaDB, and Gemini, with a locally tested Streamlit chat interface.
- Implemented structure-aware document chunking, semantic retrieval, source metadata, basic citation checks, and fallback behavior for unsupported questions.
- Evaluated retrieval and answer-generation behavior: V2 achieved **100% Hit@3 on 10 development questions**; on an **8-case RAG evaluation**, observed **80% source hit**, **80% valid citation IDs**, and **100% refusal on 3 selected unanswerable cases**; documented retrieval failures and evaluation limitations.

## CV — short version (Vietnamese)

**Enterprise AI Knowledge Assistant | Dự án AI Engineering cá nhân**

- Xây dựng ứng dụng RAG hỏi đáp tài liệu IT mẫu với Python, FastAPI, Sentence Transformers, ChromaDB, Gemini và giao diện Streamlit chạy local.
- Triển khai document chunking V1/V2, semantic search, context construction, prompt grounding, metadata trích dẫn và bộ kiểm thử Pytest.
- Đánh giá bằng dữ liệu gán nhãn; ghi nhận Source Hit Rate 80% và Citation ID Valid Rate 80% trên 5 câu có thể trả lời, cùng 3/3 trường hợp từ chối đúng trong tập đánh giá nhỏ.

## GitHub summary (English)

A multilingual enterprise IT knowledge-base assistant that retrieves semantic passages from Markdown documentation using local Sentence Transformers embeddings and ChromaDB, then generates Vietnamese answers with Google Gemini. The FastAPI backend exposes search and chat APIs; a Streamlit frontend provides interactive local chat. The repository includes chunking experiments, retrieval evaluations, basic answer guardrails, automated tests, and an honest failure-analysis report.

## Interview explanation (60–90 seconds)

> I built a document-grounded assistant for fictional enterprise IT support material. I first compared fixed-size and structure-aware chunking, then embedded the passages using a multilingual Sentence Transformers model and stored them in ChromaDB. For each question, FastAPI retrieves V2 passages, formats source-tagged context, and sends a grounding prompt to Gemini. The service returns an answer and retrieved source metadata, while Streamlit provides a chat interface. I added unit/API tests, optional similarity filtering, basic citation-ID validation, and an evaluation set with answerable and unanswerable cases. The results exposed a remote-access question where the correct VPN document was missed in top three, so my next priority is improving passage retrieval and claim-level citation verification.

## Likely interview questions and evidence-based answers

**Why RAG instead of asking Gemini directly?**

It supplies relevant source context from a controlled set of documents. This helps the model answer institution-specific questions and provides references for inspection, but it does not guarantee the model is correct.

**Why choose V2 chunking?**

V2 had stronger ranking metrics in the measured development and additional datasets. However, its advantage cannot be attributed to size alone because the embedded text also includes heading context. The additional dataset did not show a Hit@3 improvement.

**How do you handle hallucinations?**

The prompt asks the model to use only retrieved context and to refuse when evidence is insufficient; optional similarity filtering and citation-ID checking provide additional basic guardrails. These are not substitutes for sentence-level grounding evaluation or access controls.

**What was your main failure case?**

The remote-work access question did not retrieve the relevant VPN document in top three and led to a no-answer response. I would investigate query paraphrases, chunk boundaries, hybrid retrieval, reranking, and passage-level coverage.

**Is the chatbot production-ready?**

No. It is an educational portfolio prototype without authentication, fine-grained authorization, and production monitoring. Deployment and data-governance controls are important future engineering tasks.

## Claims to avoid

- “100% accurate RAG chatbot” — not supported by the evaluation.
- “Production-deployed enterprise application” — not demonstrated.
- “Verified factual citations” — current validation checks citation IDs, not whether claims are entailed by cited passages.
- “100% out-of-scope detection” — the recorded 3/3 result applies only to three selected examples.
- “Built a multi-turn conversational memory system” — the current frontend history does not automatically feed prior turns back to Gemini.
