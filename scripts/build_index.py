
from app.services.document_processor import (
    load_document_chunks
)
from app.services.embedding_service import (
    embed_texts
)
from app.services.vector_store import (
    get_collection
)


def main():
    chunks = load_document_chunks()

    if not chunks:
        print("No documents found.")
        return

    texts = [chunk["text"] for chunk in chunks]

    print(f"Processing {len(chunks)} chunks...")

    embeddings = embed_texts(texts)

    collection = get_collection()

    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in chunks
        ]
    )

    print("Database created successfully!")
    print("Total stored chunks:", collection.count())


if __name__ == "__main__":
    main()
