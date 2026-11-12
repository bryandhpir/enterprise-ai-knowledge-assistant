from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=20)

    @field_validator("question", mode="before")
    @classmethod
    def strip_question(cls, value):
        return value.strip() if isinstance(value, str) else value


class ChatSource(BaseModel):
    id: str
    source: str
    chunk_index: int
    score: float
    # Optional evidence-span indices; not a new embedding similarity score.
    context_chunk_indices: list[int] | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[ChatSource]
    model: str | None
