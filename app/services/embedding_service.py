
from functools import lru_cache
from sentence_transformers import SentenceTransformer

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@lru_cache(maxsize=1)
def get_embedding_model():
    model = SentenceTransformer(
        MODEL_NAME,
        device="cpu"
    )
    return model


def embed_texts(texts: list[str]):
    if not texts:
        raise ValueError("texts must not be empty")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings
