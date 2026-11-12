import os

import httpx
import streamlit as st

API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(page_title="Enterprise AI Knowledge Assistant", page_icon="📚", layout="centered")
st.title("📚 Enterprise AI Knowledge Assistant")
st.caption("AI-powered IT knowledge assistant using RAG, ChromaDB and Gemini.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Retrieved chunks", min_value=1, max_value=8, value=3)
    st.caption("Retrieval: ChromaDB V2")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    if not sources:
        return
    with st.expander("📄 Retrieved Sources"):
        for source in sources:
            st.markdown(f"**[{source['id']}] {source['source']}**")
            st.caption(
                f"Anchor chunk: {source['chunk_index']} | "
                f"Original-query similarity: {source['score']:.4f}"
            )
            included = source.get("context_chunk_indices") or []
            if len(included) > 1:
                st.caption(
                    "Evidence includes adjacent chunk(s): " +
                    ", ".join(str(index) for index in included)
                )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            show_sources(message["sources"])

question = st.chat_input("Ask a question about IT documentation...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = httpx.post(API_URL, json={"question": question, "top_k": top_k}, timeout=90.0)
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                sources = data.get("sources", [])
                st.markdown(answer)
                show_sources(sources)
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
            except httpx.HTTPStatusError as exc:
                st.error(f"Chat API returned HTTP {exc.response.status_code}.")
            except httpx.RequestError:
                st.error("Cannot connect to FastAPI. Please check that the backend is running.")
