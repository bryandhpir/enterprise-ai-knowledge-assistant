
from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    version="0.1.0"
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
