
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=2000
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=20
    )

    @field_validator("question", mode="before")
    @classmethod
    def strip_question(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


class ChatSource(BaseModel):
    id: str
    source: str
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[ChatSource]
    model: str | None
