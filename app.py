import streamlit as st

from src.rag_chain import ask, load_llm, load_vectorstore


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Stripe Docs AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #090d16;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #070a11;
    border-right: 1px solid #1d2636;
}


/* HEADINGS */

h1, h2, h3 {
    color: #f8fafc !important;
}

p, span, label {
    color: #cbd5e1;
}


/* HERO */

.hero-container {
    padding: 35px 10px 25px 10px;
}

.hero-label {
    color: #8b7cff;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.hero-title {
    color: white;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-top: 8px;
}

.hero-description {
    color: #94a3b8;
    font-size: 17px;
    max-width: 700px;
    line-height: 1.6;
}


/* STATUS */

.status {
    color: #4ade80;
    font-size: 14px;
    margin-top: 18px;
}


/* FEATURE CARDS */

[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

.feature-card {
    background: #101622;
    border: 1px solid #202b3d;
    border-radius: 16px;
    padding: 22px;
    min-height: 135px;
}

.feature-card:hover {
    border-color: #635bff;
}


/* CHAT */

[data-testid="stChatMessage"] {
    background: #101622;
    border: 1px solid #202b3d;
    border-radius: 16px;
    margin-bottom: 12px;
}


/* INPUT */

[data-testid="stChatInput"] {
    border: 1px solid #334155;
}


/* BUTTONS */

.stButton > button {
    background: #101622;
    border: 1px solid #263247;
    color: #cbd5e1;
    border-radius: 12px;
    min-height: 44px;
}

.stButton > button:hover {
    border-color: #635bff;
    color: white;
    background: #171d32;
}


/* DIVIDER */

hr {
    border-color: #1e293b !important;
}


/* SOURCE */

.source {
    background: #0d131f;
    border: 1px solid #202b3d;
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 8px;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE - CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# CACHE
# ============================================================

@st.cache_resource
def get_vectorstore():
    return load_vectorstore()


@st.cache_resource
def get_llm():
    return load_llm()


vectorstore = get_vectorstore()
llm = get_llm()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💳 Stripe Docs AI")

    st.caption("AI documentation assistant")

    st.success("● RAG Pipeline Online")

    st.divider()

    st.subheader("🧠 Architecture")

    st.write("📄 Stripe Documentation")
    st.write("✂️ Document Chunking")
    st.write("🔢 Hugging Face Embeddings")
    st.write("🗄️ Chroma Vector Database")
    st.write("🔍 Similarity Retrieval")
    st.write("⚡ Groq LLM")

    st.divider()

    st.subheader("🔐 Grounded AI")

    st.caption(
        "Answers are generated only from "
        "the Stripe documentation in the "
        "knowledge base."
    )

    st.divider()

    # --------------------------------------------------------
    # CLEAR CHAT BUTTON
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "LangChain • Chroma • Hugging Face • Groq"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-container">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-label">'
    'AI-POWERED DOCUMENTATION ASSISTANT'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Stripe Docs AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-description">'
    'Ask questions about Stripe and get '
    'documentation-grounded answers using '
    'Retrieval-Augmented Generation.'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="status">● RAG pipeline ready</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FEATURES
# ============================================================

st.subheader("Explore Stripe documentation")

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown("### 🔗 Webhooks")

    st.caption(
        "Understand webhook events, "
        "signatures and event handling."
    )


with c2:

    st.markdown("### 💰 Payments")

    st.caption(
        "Learn about payments, "
        "PaymentIntents and Stripe APIs."
    )


with c3:

    st.markdown("### ⚡ Stripe APIs")

    st.caption(
        "Search Stripe documentation "
        "and understand API concepts."
    )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

st.subheader("💡 Try asking")


q1, q2, q3 = st.columns(3)


with q1:

    if st.button(
        "How do webhooks work?",
        use_container_width=True,
    ):

        st.session_state.pending_question = (
            "How do Stripe webhooks work?"
        )


with q2:

    if st.button(
        "What is a PaymentIntent?",
        use_container_width=True,
    ):

        st.session_state.pending_question = (
            "What is a PaymentIntent?"
        )


with q3:

    if st.button(
        "How do I verify webhooks?",
        use_container_width=True,
    ):

        st.session_state.pending_question = (
            "How do I verify a webhook signature?"
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask anything about Stripe..."
)


if user_question:

    st.session_state.pending_question = user_question


# ============================================================
# PROCESS NEW QUESTION
# ============================================================

if st.session_state.pending_question:

    question = st.session_state.pending_question

    # Clear pending question immediately
    st.session_state.pending_question = None

    # --------------------------------------------------------
    # Add USER message to chat history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # --------------------------------------------------------
    # Get RAG answer
    # --------------------------------------------------------

    with st.spinner(
        "Searching Stripe documentation..."
    ):

        answer, sources = ask(
            question,
            vectorstore,
            llm,
        )

    # --------------------------------------------------------
    # Add ASSISTANT message to chat history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )

    # --------------------------------------------------------
    # Rerun so complete conversation is rendered together
    # --------------------------------------------------------

    st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

if st.session_state.messages:

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        role = message["role"]

        content = message["content"]

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        if role == "user":

            with st.chat_message(
                "user",
                avatar="👤",
            ):

                st.markdown(content)

        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        elif role == "assistant":

            with st.chat_message(
                "assistant",
                avatar="💳",
            ):

                st.markdown(content)

                # ------------------------------------------------
                # SOURCES FOR THIS SPECIFIC ANSWER
                # ------------------------------------------------

                sources = message.get(
                    "sources",
                    []
                )

                if sources:

                    st.divider()

                    st.markdown(
                        "#### 📚 Sources"
                    )

                    for source in sources:

                        st.markdown(
                            f"[🔗 {source}]({source})"
                        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Stripe Docs AI  •  RAG-powered documentation assistant  •  "
    "Grounded responses from Stripe documentation"
)

st.markdown(
    """
    <script>
    setTimeout(function() {
        const main = window.parent.document.querySelector('section.main');
        if (main) {
            main.scrollTo({
                top: main.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, 300);
    </script>
    """,
    unsafe_allow_html=True
    )