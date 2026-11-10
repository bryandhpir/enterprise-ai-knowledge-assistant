
import os

import httpx
import streamlit as st


API_URL = os.getenv(
    "RAG_API_URL",
    "http://127.0.0.1:8000/chat"
)


# Page configuration
st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Enterprise AI Knowledge Assistant")
st.caption(
    "AI-powered IT knowledge assistant "
    "using RAG, ChromaDB and Gemini."
)


# Sidebar configuration
with st.sidebar:
    st.header("Settings")

    top_k = st.slider(
        "Retrieved chunks",
        min_value=1,
        max_value=8,
        value=3
    )

    st.caption("Retrieval: ChromaDB V2")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    if not sources:
        return

    with st.expander("📄 Retrieved Sources"):
        for source in sources:
            st.markdown(
                f"**[{source['id']}] "
                f"{source['source']}**"
            )

            st.caption(
                f"Chunk: {source['chunk_index']} | "
                f"Similarity: {source['score']:.4f}"
            )


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            show_sources(message["sources"])


# Chat input
question = st.chat_input(
    "Ask a question about IT documentation..."
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = httpx.post(
                    API_URL,
                    json={
                        "question": question,
                        "top_k": top_k
                    },
                    timeout=90.0
                )

                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)
                show_sources(sources)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except httpx.HTTPStatusError as exc:
                st.error(
                    "Chat API returned HTTP "
                    f"{exc.response.status_code}."
                )

            except httpx.RequestError:
                st.error(
                    "Cannot connect to FastAPI. "
                    "Please check that the backend is running."
                )
