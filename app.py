"""
Stripe Docs AI Assistant
------------------------
Interactive Streamlit UI for the Stripe Documentation RAG Assistant.

Run:
    streamlit run app.py
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit Cloud support
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    except Exception:
        GROQ_API_KEY = None

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is missing.\n\n"
        "Add it to your `.env` file locally or "
        "Streamlit Cloud Secrets when deployed."
    )
    st.stop()

os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# ============================================================
# IMPORT RAG PIPELINE
# ============================================================

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src")
)

from rag_chain import load_vectorstore, ask


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Stripe Docs AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main app ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -20%,
                rgba(99, 91, 255, 0.15),
                transparent 40%
            ),
            #08080d;
    }

    .main {
        max-width: 1200px;
        margin: auto;
    }


    /* ---------- Header ---------- */

    .hero {
        text-align: center;
        padding: 45px 20px 25px 20px;
    }

    .hero-icon {
        font-size: 45px;
        margin-bottom: 8px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;

        background: linear-gradient(
            90deg,
            #ffffff,
            #a9a4ff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #9b9ba8;
        font-size: 16px;
        max-width: 700px;
        margin: auto;
        line-height: 1.6;
    }


    /* ---------- Status ---------- */

    .status-container {
        display: flex;
        justify-content: center;
        margin-top: 18px;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 6px 13px;

        border: 1px solid #272735;
        border-radius: 20px;

        background: #111119;

        color: #a8a8b5;
        font-size: 13px;
    }

    .status-dot {
        width: 8px;
        height: 8px;

        background: #36d399;
        border-radius: 50%;
    }


    /* ---------- Example cards ---------- */

    .example-title {
        text-align: center;
        color: #b7b7c5;
        font-size: 14px;
        margin-top: 25px;
        margin-bottom: 10px;
    }


    /* ---------- Chat ---------- */

    [data-testid="stChatMessage"] {
        border: 1px solid #242431;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;

        background: rgba(18, 18, 27, 0.7);
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.65;
    }


    /* ---------- Chat input ---------- */

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }


    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: #0d0d14;
        border-right: 1px solid #242431;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sidebar-description {
        color: #92929f;
        font-size: 13px;
        line-height: 1.6;
    }


    /* ---------- Tech badges ---------- */

    .tech-badge {
        display: inline-block;

        padding: 5px 9px;
        margin: 3px;

        border-radius: 7px;

        background: #171721;
        border: 1px solid #292938;

        color: #b9b9c7;
        font-size: 12px;
    }


    /* ---------- Sources ---------- */

    .source-card {
        padding: 12px 14px;

        margin-top: 8px;

        border-radius: 10px;

        background: #111119;
        border: 1px solid #292938;

        font-size: 13px;
        color: #aaaab8;
    }

    .source-label {
        color: #777786;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3px;
    }


    /* ---------- Divider ---------- */

    hr {
        border-color: #252532 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOAD RAG RESOURCES
# ============================================================

from langchain_groq import ChatGroq


@st.cache_resource
def get_llm():
    """
    Load the Groq LLM once and reuse it.
    """

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        groq_api_key=GROQ_API_KEY,
    )


@st.cache_resource
def get_resources():
    """
    Load the Chroma vector store once and reuse it.
    """

    vectorstore = load_vectorstore()

    return vectorstore


# Load resources
vectorstore = get_resources()
llm = get_llm()

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚡ Stripe Docs AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-description">
        An AI assistant that answers questions using
        your curated Stripe documentation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # System status
    st.subheader("System")

    st.success("RAG pipeline online")

    st.markdown(
        """
        <span class="tech-badge">LangChain</span>
        <span class="tech-badge">Chroma</span>
        <span class="tech-badge">HuggingFace</span>
        <span class="tech-badge">Groq</span>
        <span class="tech-badge">Streamlit</span>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Architecture
    st.subheader("Architecture")

    st.markdown(
        """
        **1. User Question**

        ↓

        **2. Hugging Face Embeddings**

        ↓

        **3. Chroma Vector Search**

        ↓

        **4. Relevant Stripe Docs**

        ↓

        **5. Groq LLM**

        ↓

        **6. Grounded Answer**
        """
    )

    st.divider()

    # RAG settings
    st.subheader("RAG Settings")

    st.markdown(
        """
        **Embedding model**

        `all-MiniLM-L6-v2`

        **Vector database**

        `Chroma`

        **LLM**

        `openai/gpt-oss-20b`

        **Retrieved chunks**

        `8`
        """
    )

    st.divider()

    # Clear chat
    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div style="padding: 30px 0 15px 0;">
        <h1 style="margin-bottom: 5px;">
            ⚡ Stripe Docs AI
        </h1>
        <p style="color: #9b9ba8; font-size: 15px;">
            Ask questions about Stripe documentation.
            Get answers grounded in your available Stripe docs.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        sources = message.get("sources", [])

        if sources:

            with st.expander(
                f"📚 Sources ({len(sources)})"
            ):

                for source in sources:

                    filename = os.path.basename(source)

                    st.markdown(
                        f"""
                        <div class="source-card">

                            <div class="source-label">
                                Stripe documentation
                            </div>

                            📄 {filename}

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# GET QUESTION
# ============================================================

question = st.chat_input(
    "Ask anything about the Stripe documentation..."
)


# Example question handling
if (
    not question
    and "example_question" in st.session_state
):

    question = st.session_state.pop(
        "example_question"
    )


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🔎 Searching Stripe documentation..."
            ):

                answer, sources = ask(
                    question,
                    vectorstore,
                    # ask() requires an LLM.
                    # rag_chain creates it through the provided object.
                    get_llm(),
                )

            st.markdown(answer)

            if sources:

                with st.expander(
                    f"📚 Sources ({len(sources)})"
                ):

                    for source in sources:

                        filename = os.path.basename(source)

                        st.markdown(
                            f"""
                            <div class="source-card">

                                <div class="source-label">
                                    Stripe documentation
                                </div>

                                📄 {filename}

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        except Exception as e:

            answer = (
                "I ran into a temporary problem while "
                "processing your question. Please try again."
            )

            sources = []

            st.error(
                f"Error: {str(e)}"
            )

            st.markdown(answer)

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )