import os

# ============================================================
# CPU OPTIMIZATION FOR STREAMLIT CLOUD
# ============================================================

# Limit CPU thread usage.
# This helps prevent CPU spikes when generating embeddings.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from typing import List, Tuple

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to .env locally or Streamlit Cloud Secrets."
    )


# ============================================================
# PATHS AND CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PERSIST_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)

# Local Hugging Face embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Groq LLM
LLM_MODEL = "openai/gpt-oss-20b"

# Number of documents retrieved from Chroma
TOP_K = 6


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Stripe Docs AI.

Your job is to answer questions using ONLY the Stripe
documentation excerpts provided below.

Rules:

1. Use only the provided Stripe documentation.
2. Do not use outside knowledge.
3. Do not guess or hallucinate.
4. If the answer cannot be found in the provided
   documentation, respond exactly:

"I couldn't find this in the Stripe docs I have access to."

5. Keep answers clear and concise.
6. Use bullet points when explaining steps.
7. Include technical details when they are present
   in the documentation.

Stripe documentation:

{context}
"""


# ============================================================
# PROMPT
# ============================================================

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)


# ============================================================
# CACHE EMBEDDING MODEL
# ============================================================

_embeddings = None


def load_embeddings():
    """
    Load the Hugging Face embedding model once.

    The model is cached in memory so it is not reloaded
    every time a question is asked.
    """

    global _embeddings

    if _embeddings is None:

        # ----------------------------------------------------
        # Limit PyTorch CPU threads
        # ----------------------------------------------------

        import torch

        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)

        # ----------------------------------------------------
        # Load embedding model
        # ----------------------------------------------------

        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    return _embeddings


# ============================================================
# CACHE VECTOR STORE
# ============================================================

_vectorstore = None


def load_vectorstore():
    """
    Load the existing Chroma vector database.

    IMPORTANT:
    This does NOT rebuild the vector database.

    The collection name MUST match the collection used
    inside build_vectorstore.py.
    """

    global _vectorstore

    if _vectorstore is None:

        embeddings = load_embeddings()

        _vectorstore = Chroma(
            collection_name="stripe_docs",
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings,
        )

    return _vectorstore


# ============================================================
# CACHE GROQ LLM
# ============================================================

_llm = None


def load_llm():
    """
    Load the Groq LLM once and reuse it.
    """

    global _llm

    if _llm is None:

        _llm = ChatGroq(
            model=LLM_MODEL,
            temperature=0.2,
            groq_api_key=GROQ_API_KEY,
            max_retries=2,
        )

    return _llm


# ============================================================
# FORMAT RETRIEVED DOCUMENTS
# ============================================================

def format_context(docs: List[Document]) -> str:
    """
    Convert retrieved documents into context
    that will be given to the LLM.
    """

    if not docs:
        return ""

    context_parts = []

    for i, doc in enumerate(docs, start=1):

        source = doc.metadata.get(
            "source",
            "Unknown source"
        )

        context_parts.append(
            f"""
--- Document {i} ---

Source: {source}

{doc.page_content}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# EXTRACT SOURCE URL
# ============================================================

def extract_source_url(doc: Document):
    """
    Try to find the original Stripe documentation URL.

    First:
    Check Chroma metadata.

    If not found:
    Search inside the document content for:

    Source: https://...
    """

    # --------------------------------------------------------
    # Try metadata first
    # --------------------------------------------------------

    source = doc.metadata.get("source")

    if source and str(source).startswith("http"):
        return str(source)

    # --------------------------------------------------------
    # Fallback: search inside document content
    # --------------------------------------------------------

    for line in doc.page_content.splitlines():

        line = line.strip()

        if line.startswith("Source:"):

            url = line.replace(
                "Source:",
                "",
                1
            ).strip()

            if url.startswith("http"):
                return url

    return None


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(
    question: str,
    vectorstore
) -> List[Document]:
    """
    Retrieve the most relevant Stripe documentation
    chunks from Chroma.
    """

    return vectorstore.similarity_search(
        question,
        k=TOP_K
    )


# ============================================================
# MAIN RAG FUNCTION
# ============================================================

def ask(
    question: str,
    vectorstore=None,
    llm=None
) -> Tuple[str, List[str]]:
    """
    Complete RAG pipeline:

    Question
       ↓
    Chroma Retrieval
       ↓
    Relevant Stripe Docs
       ↓
    Prompt
       ↓
    Groq LLM
       ↓
    Grounded Answer + Sources
    """

    # --------------------------------------------------------
    # Clean question
    # --------------------------------------------------------

    question = question.strip()

    if not question:

        return (
            "Please enter a question.",
            []
        )

    # --------------------------------------------------------
    # Load resources if not provided
    # --------------------------------------------------------

    if vectorstore is None:
        vectorstore = load_vectorstore()

    if llm is None:
        llm = load_llm()

    # --------------------------------------------------------
    # Retrieve relevant documents
    # --------------------------------------------------------

    docs = retrieve_documents(
        question,
        vectorstore
    )

    # --------------------------------------------------------
    # No documents found
    # --------------------------------------------------------

    if not docs:

        return (
            "I couldn't find this in the Stripe docs I have access to.",
            []
        )

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context = format_context(docs)

    # --------------------------------------------------------
    # Create RAG chain
    # --------------------------------------------------------

    chain = PROMPT | llm

    # --------------------------------------------------------
    # Send question + context to Groq
    # --------------------------------------------------------

    response = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )

    answer = response.content

    # --------------------------------------------------------
    # Extract sources
    # --------------------------------------------------------

    sources = []

    for doc in docs:

        source = extract_source_url(doc)

        if source and source not in sources:

            sources.append(source)

    return answer, sources


# ============================================================
# COMMAND-LINE TEST
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 50)
    print("        STRIPE DOCS AI")
    print("=" * 50)

    print("\nLoading resources...")

    vectorstore = load_vectorstore()
    llm = load_llm()

    print("Resources loaded successfully.")
    print("\nType 'exit' or 'quit' to stop.")
    print("-" * 50)

    # --------------------------------------------------------
    # CONTINUOUS QUESTION LOOP
    # --------------------------------------------------------

    while True:

        question = input("\nAsk a Stripe question: ").strip()

        # ----------------------------------------------------
        # Exit condition
        # ----------------------------------------------------

        if question.lower() in ["exit", "quit"]:

            print("\nGoodbye! 👋")
            break

        # ----------------------------------------------------
        # Empty question
        # ----------------------------------------------------

        if not question:

            print("Please enter a question.")

            continue

        # ----------------------------------------------------
        # Run RAG
        # ----------------------------------------------------

        answer, sources = ask(
            question,
            vectorstore,
            llm
        )

        # ----------------------------------------------------
        # Display answer
        # ----------------------------------------------------

        print("\nAssistant:")
        print("-" * 50)

        print(answer)

        # ----------------------------------------------------
        # Display sources
        # ----------------------------------------------------

        print("\nSources:")
        print("-" * 50)

        if sources:

            for source in sources:

                print(f"- {source}")

        else:

            print("- No source URL found.")

        print("-" * 50)