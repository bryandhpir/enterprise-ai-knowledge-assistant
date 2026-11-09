
def build_context(chunks: list[dict]) -> str:
    context_parts = []

    for chunk in chunks:
        text = chunk["text"].strip()

        if not text:
            continue

        reference_id = f"S{len(context_parts) + 1}"

        formatted_chunk = (
            f"[{reference_id}]\n"
            f"Source: {chunk['source']}\n"
            f"Chunk index: {chunk['chunk_index']}\n"
            f"Content:\n{text}"
        )

        context_parts.append(formatted_chunk)

    return "\n\n".join(context_parts)
