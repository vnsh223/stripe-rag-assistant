"""
Stripe Docs RAG Assistant - Streamlit UI
--------------------------------------------
A simple chat interface over the RAG pipeline built in src/rag_chain.py.
Run with: streamlit run app.py
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Resolve the API key BEFORE importing rag_chain, since that module checks
# for GOOGLE_API_KEY as soon as it's imported. Locally it comes from .env;
# on Streamlit Cloud it comes from the app's Secrets settings instead.
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)

if not GOOGLE_API_KEY:
    st.error(
        "GOOGLE_API_KEY not found. Set it in your .env file locally, "
        "or in Streamlit Cloud's Secrets settings when deployed."
    )
    st.stop()

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Allow importing from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from rag_chain import load_vectorstore, ask
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(
    page_title="Stripe Docs Assistant",
    page_icon="💳",
    layout="centered",
)

# ---- Custom styling ----
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #14121f 100%);
    }
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 4px 8px;
    }
    h1 {
        background: linear-gradient(90deg, #635bff, #a29bfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .stChatInput textarea {
        border-radius: 12px !important;
    }
    [data-testid="stSidebar"] {
        background: #14121f;
        border-right: 1px solid #2a2740;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #2a2740;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Cache the vector store + LLM so they load once, not on every rerun ----
@st.cache_resource
def get_resources():
    vectorstore = load_vectorstore()
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )
    return vectorstore, llm


vectorstore, llm = get_resources()

# ---- Header ----
st.title("💳 Stripe Docs Assistant")
st.markdown(
    "`LangChain` `Gemini` `Chroma` `RAG`"
)
st.caption(
    "Ask a question about Stripe payments, checkout, subscriptions, "
    "webhooks, or refunds. Answers are grounded strictly in Stripe's "
    "documentation — if it's not in the docs, the assistant will say so "
    "instead of guessing."
)
st.divider()

# ---- Chat history state ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Render existing chat history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- `{os.path.basename(s)}`")

# ---- Chat input ----
question = st.chat_input("Ask about Stripe payments, checkout, webhooks...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the docs..."):
            try:
                answer, sources = ask(question, vectorstore, llm)
            except Exception as e:
                answer = (
                    "Something went wrong answering that — this is likely "
                    "a temporary rate limit on the free Gemini tier. "
                    "Please wait a few seconds and try again."
                )
                sources = []
                st.error(f"Debug detail: {e}")

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for s in sources:
                    st.markdown(f"- `{os.path.basename(s)}`")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

# ---- Sidebar ----
with st.sidebar:
    st.header("About this project")
    st.markdown(
        """
This is a **Retrieval-Augmented Generation (RAG)** assistant built with:
- **LangChain** for the retrieval + generation pipeline
- **Chroma** as the vector database
- **Google Gemini** for embeddings and answer generation
- **Streamlit** for this interface

It's grounded in a curated set of Stripe's public documentation
(payments, checkout, subscriptions, webhooks, disputes & refunds),
and refuses to answer questions outside that scope instead of
hallucinating.
        """
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()