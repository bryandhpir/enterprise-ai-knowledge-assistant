
from app.services.document_processor_v2 import (
    load_document_chunks_v2
)

from app.services.embedding_service import (
    embed_texts
)

from app.services.vector_store import (
    get_collection
)


COLLECTION_NAME = "it_knowledge_base_v2"
BATCH_SIZE = 32


def main():
    chunks = load_document_chunks_v2()

    if not chunks:
        print("No chunks found.")
        return

    print(f"Processing {len(chunks)} V2 chunks...")

    collection = get_collection(COLLECTION_NAME)

    # Clear only the V2 collection's existing records
    old_ids = collection.get()["ids"]

    if old_ids:
        collection.delete(ids=old_ids)

    # Generate and store embeddings in batches
    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        texts = [item["text"] for item in batch]
        embeddings = embed_texts(texts)

        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=[
                {
                    "source": item["source"],
                    "chunk_index": item["chunk_index"]
                }
                for item in batch
            ]
        )

        print(
            f"Indexed {min(start + BATCH_SIZE, len(chunks))}"
            f"/{len(chunks)} chunks"
        )

    print("\nV2 indexing completed!")
    print("Collection:", COLLECTION_NAME)
    print("Total stored chunks:", collection.count())


if __name__ == "__main__":
    main()
