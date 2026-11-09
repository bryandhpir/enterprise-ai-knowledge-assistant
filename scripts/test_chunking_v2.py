
from app.services.document_processor import (
    load_document_chunks
)

from app.services.document_processor_v2 import (
    load_document_chunks_v2
)


old_chunks = load_document_chunks()
new_chunks = load_document_chunks_v2()

print("V1 total chunks:", len(old_chunks))
print("V2 total chunks:", len(new_chunks))

print("\nFirst V2 chunk:")
print(new_chunks[0]["text"])

print("\nMetadata:")
print({
    "id": new_chunks[0]["id"],
    "source": new_chunks[0]["source"],
    "chunk_index": new_chunks[0]["chunk_index"]
})
