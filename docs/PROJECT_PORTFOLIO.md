# AI Engineering Portfolio — Hà Bảo Nguyên

**AI Engineer Intern / Fresher · Python · RAG · Applied Machine Learning · MLOps**  
Da Nang, Vietnam · [Email](mailto:nguyenha.300102@gmail.com) · [GitHub](https://github.com/bryandhpir)

I have completed the Information Technology coursework at the University of Danang – Vietnam-Korea University (VKU); degree conferral is pending the English exit requirement. My personal projects emphasize traceable experiments, data validation, working Python services, and practical engineering trade-offs.

> **Project scope:** Both systems are portfolio prototypes. All reported metrics come from documented, small-scale or offline local evaluations; they are not independently validated production accuracy or deployment claims.

## Featured projects

### 1. [Enterprise AI Knowledge Assistant](https://github.com/bryandhpir/enterprise-ai-knowledge-assistant)

**Vietnamese-answering retrieval-augmented IT documentation assistant · 2026**

**Stack:** Python, FastAPI, Pydantic, Sentence Transformers, ChromaDB, Google Gemini API, Streamlit, Docker Compose, Pytest, GitHub Actions.

**Challenge:** Answer questions about a small collection of sample internal IT guides with traceable source IDs, while identifying unanswered cases and retrieval failures.

**What I implemented**

- Parsed five fictional Markdown knowledge guides and compared fixed-window with section/paragraph-aware chunking; embedded the text with a multilingual Sentence Transformers model and stored it in persistent ChromaDB.
- Built a FastAPI chatbot with a Streamlit interface, source-tagged evidence, Gemini answer generation, optional similarity threshold, citation-ID checks, and an insufficient-evidence fallback.
- Compared three configurable retrieval modes: semantic baseline, experimental Multi-Query Retrieval with weighted Reciprocal Rank Fusion (RRF), and BM25-style lexical reranking over an expanded semantic candidate set.
- Added optional *same-section neighboring chunk expansion* so a top-ranked passage can include the continuation of its section without changing the retrieval ranking or inventing additional similarity scores.
- Containerized API and frontend services with Docker Compose and persistent volumes; automated Python tests and Docker image builds using GitHub Actions.
- Maintained structured passage-level and end-to-end evaluation scripts, saved result files, and a qualitative review of generated answers.

**Recorded evaluation — small curated development data**

| Observation | Result | Scope |
| --- | --- | --- |
| Passage Hit@3, dense retrieval | 5/8 (**62.5%**) | Eight labeled development questions |
| Passage Hit@3, lexical reranking | 8/8 (**100%**) | Same questions, 80 candidates / lexical weight 0.65 |
| Passage MRR@3 | **0.4583 → 0.7917** | Dense versus reranked passages |
| Valid citation IDs, end-to-end | **5/8 → 8/8** | A separate 12-case run; eight answerable questions |
| Manually assessed complete answers | **4/8 → 7/8** | Reranking alone versus reranking plus neighbors, one recorded run |

**Trade-offs:** The correct source filename is not always the correct passage. Neighbor expansion helped with a split MFA-recovery instruction and a device-handover checklist, but it increases context size, and latency varied considerably across API calls. Valid citation IDs do not prove that a generated claim is supported. This is not an access-controlled enterprise deployment.

**Repository evidence:** [Project README](https://github.com/bryandhpir/enterprise-ai-knowledge-assistant) · [Passage evaluation](https://github.com/bryandhpir/enterprise-ai-knowledge-assistant/blob/main/evals/reports/passage_rerank_eval.json) · [Neighbor answer review](https://github.com/bryandhpir/enterprise-ai-knowledge-assistant/blob/main/docs/NEIGHBOR_CONTEXT_MANUAL_REVIEW.md) · [CI workflow](https://github.com/bryandhpir/enterprise-ai-knowledge-assistant/actions).

### 2. [Sales Forecasting & MLOps Platform](https://github.com/bryandhpir/sales-forecasting-mlops-platform)

**Retail unit-sales forecasting, time-aware model evaluation, and reproducible ML engineering · 2026**

**Stack:** Python, Pandas, NumPy, scikit-learn, SciPy, MLflow Tracking/Registry, FastAPI, Docker Compose, Pytest, GitHub Actions.

**Challenge:** Forecast sales by store and product family without accidentally using observed values that would have been unavailable at the forecast cutoff.

**What I implemented**

- Processed **3,000,888** historical Kaggle Store Sales records spanning **54 stores** and **33 product families**, with validation and reproducible data transformations.
- Engineered calendar, lag and rolling history features; constructed training and prediction examples using cutoff-safe historical snapshots and time-aware rolling-origin backtesting.
- Trained **HistGradientBoostingRegressor** with log-transformed target values and tracked/registered model artifacts with MLflow.
- Created a FastAPI `/predict` endpoint for store–family unit-sales forecasts with a configurable horizon within the model's evaluated limit.
- Added Docker Compose services for the API and MLflow, and GitHub Actions CI covering Python tests, container builds, and an API health check.
- Developed **offline historical monitoring** for Kolmogorov–Smirnov (KS) feature-drift diagnostics and performance breakdowns by store, product family, cutoff, and forecast step.

**Saved offline backtesting result — one specified run**

| Metric | Result |
| --- | ---: |
| Dataset rows | **3,000,888** |
| Evaluation origins | **3** |
| Horizon evaluated | **7 calendar days** |
| Scored target observations | **37,422** |
| Scored-target coverage | **100%** |
| MAE | **79.01 sales units** |
| RMSLE | **0.4488** |

**Trade-offs:** These values describe an offline historical run and should not be interpreted as accuracy guaranteed for future stores or dates. Scored-target coverage means eligible observed targets were scored; it is **not** statistical prediction-interval coverage. Drift monitoring is historical and offline, not a live alerting system. The project is not a cloud production forecasting service.

**Repository evidence:** [Source and tests](https://github.com/bryandhpir/sales-forecasting-mlops-platform) · [Model training guide](https://github.com/bryandhpir/sales-forecasting-mlops-platform/blob/main/docs/MODEL_TRAINING.md) · [API implementation](https://github.com/bryandhpir/sales-forecasting-mlops-platform/blob/main/src/api.py) · [CI workflow](https://github.com/bryandhpir/sales-forecasting-mlops-platform/actions).

## Additional projects

| Project | Practical focus |
| --- | --- |
| **E-commerce Data Warehouse** · Academic · 2023 | SQL Server, SSIS, star-schema dimensional modeling, ETL, FactOrders and data-quality checks |
| **Fashion E-commerce Data Analysis** · Project assistance · 2025 | Data preparation and statistical analysis over 44,424 product records; two-way ANOVA on 26,752 complete cases |
| **Laptop & Technology E-commerce Platform** · Graduation thesis · 2024 | Django/SQLite application with accounts, catalog, order administration and real-time chat |

## Technical skills

- **Programming and data:** Python, SQL, Pandas, NumPy, SQL Server, SSMS, SSIS/ETL, SQLite, MySQL; Java and JavaScript/TypeScript fundamentals.
- **AI and machine learning:** Retrieval-Augmented Generation, semantic retrieval, Sentence Transformers, ChromaDB, Gemini API, lexical reranking, scikit-learn, time-aware forecasting, model evaluation.
- **Backend and MLOps:** FastAPI, Pydantic, Streamlit, REST APIs, MLflow Tracking/Registry, Docker Compose, GitHub Actions, Pytest, offline drift diagnostics.

## Experience and education

**Owner / Business Operator — AB Medical Grocery (2024–2025):** Small online retail operation, including sourcing, customer support, order handling, shipment tracking, inventory and financial records.

**The University of Danang – Vietnam-Korea University (VKU), Information Technology (2020–2025):** Coursework completed; degree not yet conferred because the English exit requirement is pending.

**FPT Global Software Talent:** Java Web Advance training, 88 hours; certificate `FA.DN.GST_2023.032`.

## Interview summary

> I developed two personal AI engineering projects that cover both LLM-based applications and conventional machine learning. For the RAG assistant, I tested document chunking, semantic search, query expansion, lexical reranking and neighboring context against labeled IT-support queries, then integrated FastAPI, Streamlit, Docker and CI. For the forecasting platform, I built cutoff-safe features and rolling-origin backtesting over a multi-store retail dataset, trained a Gradient Boosting model, tracked experiments with MLflow, served predictions through FastAPI and added container-based CI. I documented the measured outcomes alongside their limitations rather than treating a small experiment as production validation.

---

**Project status:** Working personal prototypes. Neither project demonstrates enterprise adoption, authenticated multi-tenant deployment, general production accuracy or cloud CD.
