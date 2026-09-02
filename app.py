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
# THEME
# ============================================================

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500&display=swap" rel="stylesheet">

<style>

:root {
    --bg: #0a0714;
    --panel: #12101f;
    --panel-2: #171425;
    --border: #262038;
    --text: #f1eef9;
    --text-muted: #928da8;
    --accent-1: #7c6bff;
    --accent-2: #ff6ec7;
    --mono: 'JetBrains Mono', monospace;
    --display: 'Space Grotesk', sans-serif;
}

.stApp {
    background: var(--bg);
}

.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

p, span, label, li { color: var(--text-muted); font-family: 'Inter', sans-serif; }
h1, h2, h3 { color: var(--text) !important; font-family: var(--display); }
hr { border-color: var(--border) !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #07050f;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h1 { font-size: 20px; }

.sb-tag {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-muted);
    padding: 3px 0;
}

.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #34d399;
    margin-right: 7px;
    box-shadow: 0 0 8px #34d399;
}

/* HERO */
.hero-title {
    font-family: var(--display);
    font-weight: 700;
    font-size: 46px;
    line-height: 1.08;
    letter-spacing: -0.5px;
    color: var(--text);
    background: linear-gradient(100deg, var(--text) 55%, var(--accent-1) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 16px;
    color: var(--text-muted);
    max-width: 520px;
    line-height: 1.65;
    margin-top: 14px;
}

/* TERMINAL PREVIEW CARD */
.term-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    font-family: var(--mono);
    font-size: 13px;
}
.term-head {
    display: flex;
    gap: 6px;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    background: var(--panel-2);
}
.term-dot { width: 9px; height: 9px; border-radius: 50%; background: #34344a; }
.term-body { padding: 16px; color: #b9b4d1; }
.term-q { color: var(--accent-2); }
.term-a { color: #9ce8c9; margin-top: 8px; display: block; }

/* SUGGESTION CHIPS as buttons */
.stButton > button {
    background: var(--panel);
    border: 1px solid var(--border);
    color: var(--text-muted);
    border-radius: 10px;
    font-family: var(--mono);
    font-size: 13px;
    padding: 10px 14px;
    min-height: 0;
}
.stButton > button:hover {
    border-color: var(--accent-1);
    color: var(--text);
    background: var(--panel-2);
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    border: 1px solid var(--border);
    border-radius: 12px;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent-1);
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    margin-bottom: 10px;
}

.src-chip {
    display: inline-block;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--accent-1);
    background: rgba(124,107,255,0.1);
    border: 1px solid rgba(124,107,255,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    margin: 4px 6px 0 0;
    text-decoration: none;
}

.footer {
    text-align: center;
    font-family: var(--mono);
    color: #3d3856;
    font-size: 12px;
    margin-top: 60px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
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
    st.caption("Documentation-grounded answers")

    st.markdown(
        '<div style="margin: 14px 0;">'
        '<span class="status-dot"></span>'
        '<span class="sb-tag">pipeline online</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("**Pipeline**")
    for step in [
        "Stripe documentation",
        "Chunking",
        "HF embeddings",
        "Chroma vector DB",
        "Similarity retrieval",
        "Groq LLM",
    ]:
        st.markdown(f'<div class="sb-tag">→ {step}</div>', unsafe_allow_html=True)

    st.divider()
    st.caption(
        "Answers are generated only from the Stripe "
        "documentation in the knowledge base — no outside "
        "guessing."
    )

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sb-tag" style="margin-top:20px; opacity:0.6;">'
        'LangChain · Chroma · HF · Groq</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown('<div class="hero-title">Ask the Stripe<br>docs directly.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Retrieval-augmented answers pulled straight from '
        'Stripe\'s documentation — every response traced back to its source, '
        'nothing invented.</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="term-card">
            <div class="term-head">
                <div class="term-dot"></div><div class="term-dot"></div><div class="term-dot"></div>
            </div>
            <div class="term-body">
                <span class="term-q">$ ask "how do webhooks work?"</span>
                <span class="term-a">→ Stripe sends an HTTP POST to your
                endpoint when an event occurs...</span>
                <br><span style="color:#5c5678;">— source: docs/webhooks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ============================================================
# SUGGESTED QUESTIONS (functional chips)
# ============================================================

q1, q2, q3 = st.columns(3)
with q1:
    if st.button("How do webhooks work?", use_container_width=True):
        st.session_state.pending_question = "How do Stripe webhooks work?"
with q2:
    if st.button("What is a PaymentIntent?", use_container_width=True):
        st.session_state.pending_question = "What is a PaymentIntent?"
with q3:
    if st.button("How do I verify webhooks?", use_container_width=True):
        st.session_state.pending_question = "How do I verify a webhook signature?"

st.write("")

# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input("Ask anything about Stripe...")
if user_question:
    st.session_state.pending_question = user_question


# ============================================================
# PROCESS NEW QUESTION
# ============================================================

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("Searching Stripe documentation..."):
        answer, sources = ask(question, vectorstore, llm)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
    st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

if st.session_state.messages:
    st.divider()
    st.markdown("### Conversation")

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)

        elif role == "assistant":
            with st.chat_message("assistant", avatar="💳"):
                st.markdown(content)

                sources = message.get("sources", [])
                if sources:
                    chips = "".join(
                        f'<a class="src-chip" href="{s}" target="_blank">📄 {s}</a>'
                        for s in sources
                    )
                    st.markdown(chips, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">stripe docs ai — rag-powered · grounded in documentation only</div>',
    unsafe_allow_html=True,
)