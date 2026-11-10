# Demo Guide — Enterprise AI Knowledge Assistant

A concise walkthrough for reviewers, interviews, and portfolio recordings. Use fabricated/sample documents only.

## Start the app locally

Open two PowerShell terminals in the repository root.

**Backend:**

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Frontend:**

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

- Chat UI: http://localhost:8501
- Swagger UI: http://127.0.0.1:8000/docs

If `/chat` returns errors, confirm `.env` is configured and `it_knowledge_base_v2` is indexed. The frontend source file must exist locally; it may still need to be committed to the remote repository.

## Demonstration sequence

| Scenario | Ask | What to show |
| --- | --- | --- |
| Document-grounded assistance | `Làm thế nào để kết nối VPN vào mạng nội bộ công ty?` | A Vietnamese response with references to `vpn_access.md` |
| Another IT procedure | `Tài khoản công ty bị khóa thì tôi cần làm gì?` | The answer and retrieved source metadata; check whether Helpdesk guidance is complete |
| Out-of-scope handling | `Giá vàng SJC hiện tại là bao nhiêu?` | A no-answer response rather than fabricated live pricing |
| Chat usability | Ask two independent questions and use `Clear conversation` | Streamlit chat history clears; model context is not multi-turn by default |

These are demonstration scenarios, not guarantees. Generated content can vary; inspect output before recording.

## Suggested recording structure (about 2–3 minutes)

1. **Problem (15 seconds):** Employees need to locate IT procedures even when questions differ from document wording.
2. **Architecture (25 seconds):** Explain Sentence Transformers → ChromaDB V2 → context/prompt → Gemini → FastAPI/Streamlit.
3. **Live chat (60 seconds):** Ask one VPN question and expand retrieved source references.
4. **Boundary test (20 seconds):** Ask a question that is not covered by the knowledge base; show the refusal behavior.
5. **Evidence (30 seconds):** Show the recorded evaluation table and note the remote-access retrieval failure.
6. **Closing (15 seconds):** Explain that it is a local educational prototype, not a deployed enterprise service.

## Screenshots to capture

Create the directory `docs/images/` in your working repository and capture real images from your application:

- `chatbot_demo.png`: Chat answer with visible citation markers and source expander.
- `chatbot_no_answer.png`: An out-of-scope or unavailable-information response.
- `swagger_chat.png`: `POST /chat` request and response schema (optional).

Avoid screenshots showing API keys, private browser tabs, OS usernames, personal information, or confidential documents. No screenshot is bundled with this documentation because the running interface was not available to capture here.

Once the screenshot exists, insert this into the project README:

```markdown
![Enterprise AI Knowledge Assistant interface](docs/images/chatbot_demo.png)
```

## Pre-publication checklist

- [ ] `frontend/streamlit_app.py` is committed (it was not visible on the last checked remote branch).
- [ ] `requirements.txt` lists tested versions of `chromadb` and `streamlit`.
- [ ] README instructions work from a fresh environment.
- [ ] Local `.env` remains ignored and untracked.
- [ ] Full evaluation report corresponds to the **8-question** dataset, not a two-question preview.
- [ ] All automated tests pass locally.
- [ ] Screenshots show real behavior and do not overstate model accuracy.
