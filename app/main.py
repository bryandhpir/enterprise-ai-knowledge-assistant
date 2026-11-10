import logging
import os
import time

from fastapi import Request

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_question
from google.genai import errors
from fastapi import FastAPI
from app.services.readiness import is_ready


log_level = os.getenv("LOG_LEVEL", "INFO").upper()

if log_level not in {
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
}:
    log_level = "INFO"

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger("enterprise_ai")


app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    version="0.1.0"
)
@app.middleware("http")
async def request_logging(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "http method=%s path=%s status=%s duration_ms=%.1f",
            request.method,
            request.url.path,
            status_code,
            duration_ms
        )
        
@app.get("/")
def home():
    return {"message": "Welcome to Knowledge Assistant"}

@app.get("/health")
def health():
    return {"status": "ok"}

from pathlib import Path
from fastapi import Query

DOCS_DIR = Path(__file__).resolve().parent.parent / "sample_docs"

@app.get("/documents")
def list_documents():
    files = sorted(DOCS_DIR.glob("*.md"))

    return {
        "total": len(files),
        "documents": [file.name for file in files]
    }

@app.get("/search")
def search_documents(q: str = Query(min_length=2)):
    results = []

    for file in DOCS_DIR.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        if q.casefold() in content.casefold():
            results.append({
                "filename": file.name,
                "preview": content[:200]
            })

    return {
        "query": q,
        "total": len(results),
        "results": results
    }

from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.services.chroma_search import search_chroma


class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=3, ge=1, le=20)


@app.post("/semantic-search")
def semantic_search_endpoint(
    request: SemanticSearchRequest
):
    if not request.query.strip():
        raise HTTPException(
            status_code=422,
            detail="Query must not be empty"
        )

    results = search_chroma(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "total": len(results),
        "results": results
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        result = answer_question(
            question=request.question,
            top_k=request.top_k
        )

        return result

    except errors.APIError as exc:
        raise HTTPException(
            status_code=502,
            detail="Dịch vụ AI hiện không khả dụng. Vui lòng thử lại sau."
        ) from exc


@app.get("/ready")
def readiness_endpoint():
    try:
        ready = is_ready()
    except Exception:
        logger.exception("Readiness check failed")
        ready = False

    if not ready:
        raise HTTPException(
            status_code=503,
            detail="Service not ready"
        )

    return {"status": "ready"}
