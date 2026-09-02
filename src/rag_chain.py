"""
Stripe Docs AI Assistant - RAG Chain
------------------------------------

Core Retrieval-Augmented Generation (RAG) pipeline.

Flow:

User Question
      ↓
Hugging Face Embedding
      ↓
Chroma Vector Search
      ↓
Top relevant Stripe documentation chunks
      ↓
Groq LLM
      ↓
Grounded Answer + Sources

Technologies:
- LangChain
- Hugging Face Embeddings
- Chroma
- Groq
"""


# ============================================================
# IMPORTS
# ============================================================

import os
import time

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found.\n"
        "Please add GROQ_API_KEY to your .env file."
    )


if GROQ_API_KEY == "your_groq_api_key_here":
    raise ValueError(
        "GROQ_API_KEY is still using the placeholder value.\n"
        "Please add your real Groq API key to .env."
    )


# ============================================================
# CONFIGURATION
# ============================================================

# Location of the Chroma database
PERSIST_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db",
)


# Number of relevant chunks retrieved from Chroma
TOP_K = 8


# Same embedding model used when Chroma was built
EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Groq model
LLM_MODEL = "openai/gpt-oss-20b"


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Stripe Docs AI, a developer support assistant.

Your job is to answer questions using ONLY the Stripe
documentation excerpts provided below.

IMPORTANT RULES:

1. Use ONLY the provided documentation excerpts.

2. Do NOT use outside knowledge about Stripe, payments,
   APIs, programming, or other topics.

3. Do NOT guess or invent information.

4. If the documentation contains enough information,
   answer clearly and practically.

5. If the documentation contains only part of the answer,
   explain only the information supported by the excerpts.

6. If the documentation does NOT contain enough information
   to answer the question, respond exactly:

"I couldn't find this in the Stripe docs I have access to."

7. Keep answers focused and useful for developers.

8. For technical questions, use bullet points or numbered
   steps when appropriate.

9. Do not invent Stripe API names, parameters, endpoints,
   events, products, or implementation details.

10. Do not use information from the source URL itself.
    Use only the documentation text provided in the excerpts.

Stripe documentation excerpts:

{context}
"""


# ============================================================
# LOAD HUGGING FACE EMBEDDINGS + CHROMA
# ============================================================

def load_vectorstore():
    """
    Load the existing Chroma vector database.

    The Chroma database was created using:

        sentence-transformers/all-MiniLM-L6-v2

    Returns:
        Chroma vector store
    """

    print("Loading Hugging Face embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Loading Chroma vector store...")

    vectorstore = Chroma(
        collection_name="stripe_docs",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )

    return vectorstore


# ============================================================
# LOAD GROQ LLM
# ============================================================

def load_llm():
    """
    Create and return the Groq language model.
    """

    print("Loading Groq LLM...")

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.2,
        groq_api_key=GROQ_API_KEY,
    )

    return llm


# ============================================================
# FORMAT RETRIEVED DOCUMENTS
# ============================================================

def format_context(docs):
    """
    Convert retrieved documents into context for the LLM.

    Each Markdown document begins with something like:

        Source: https://docs.stripe.com/webhooks

    The retrieved text is passed to the LLM together with
    the source information.
    """

    blocks = []

    for i, doc in enumerate(docs, start=1):

        source_file = doc.metadata.get(
            "source",
            "unknown source"
        )

        content = doc.page_content.strip()

        blocks.append(
            f"[Excerpt {i}]\n"
            f"Source file: {source_file}\n\n"
            f"{content}"
        )

    return "\n\n".join(blocks)


# ============================================================
# EXTRACT ORIGINAL STRIPE DOCUMENTATION URL
# ============================================================

def extract_source_url(doc):
    """
    Extract the original Stripe documentation URL from
    the beginning of the Markdown document.

    Example:

        Source: https://docs.stripe.com/webhooks

    Returns:
        Stripe documentation URL
        or None if no valid Stripe URL is found.
    """

    content = doc.page_content.strip()

    if not content:
        return None

    lines = content.splitlines()

    if not lines:
        return None

    first_line = lines[0].strip()

    if not first_line.startswith("Source:"):
        return None

    url = first_line.replace(
        "Source:",
        "",
        1
    ).strip()

    if url.startswith(
        "https://docs.stripe.com/"
    ):
        return url

    return None


# ============================================================
# RETRIEVAL WITH RETRY
# ============================================================

def retrieve_with_retry(
    retriever,
    question,
    max_attempts=3,
):
    """
    Retrieve relevant documents from Chroma.

    Retries temporary retrieval errors up to max_attempts.
    """

    attempt = 0

    while True:

        try:

            return retriever.invoke(question)

        except Exception as error:

            attempt += 1

            if attempt >= max_attempts:
                raise error

            wait_time = 3 * attempt

            print(
                f"Temporary retrieval error: {error}"
            )

            print(
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


# ============================================================
# ASK QUESTION
# ============================================================

def ask(
    question: str,
    vectorstore,
    llm,
):
    """
    Execute the complete RAG pipeline.

    Args:
        question:
            User's question.

        vectorstore:
            Chroma vector database.

        llm:
            Groq language model.

    Returns:
        answer:
            Grounded answer generated by the LLM.

        sources:
            List of original Stripe documentation URLs.
    """

    # --------------------------------------------------------
    # 1. Create retriever
    # --------------------------------------------------------

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )


    # --------------------------------------------------------
    # 2. Retrieve relevant documentation
    # --------------------------------------------------------

    docs = retrieve_with_retry(
        retriever,
        question,
    )


    # --------------------------------------------------------
    # 3. Handle no retrieved documents
    # --------------------------------------------------------

    if not docs:

        return (
            "I couldn't find this in the Stripe docs "
            "I have access to.",
            [],
        )


    # --------------------------------------------------------
    # 4. Format retrieved context
    # --------------------------------------------------------

    context = format_context(docs)


    # --------------------------------------------------------
    # 5. Create prompt
    # --------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )


    # --------------------------------------------------------
    # 6. Create LangChain chain
    # --------------------------------------------------------

    chain = prompt | llm


    # --------------------------------------------------------
    # 7. Generate grounded answer
    # --------------------------------------------------------

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )


    # --------------------------------------------------------
    # 8. Extract Stripe documentation URLs
    # --------------------------------------------------------

    sources = []

    for doc in docs:

        url = extract_source_url(doc)

        if url and url not in sources:
            sources.append(url)


    # --------------------------------------------------------
    # 9. Return answer + sources
    # --------------------------------------------------------

    return response.content, sources


# ============================================================
# TERMINAL TEST
# ============================================================

def main():
    """
    Run the RAG assistant directly from the terminal.

    This allows us to test the backend independently from
    Streamlit.
    """

    print()
    print("=" * 60)
    print("        STRIPE DOCS AI - RAG ASSISTANT")
    print("=" * 60)
    print()

    # Load Chroma
    print("Initializing vector store...")

    vectorstore = load_vectorstore()

    # Load Groq
    llm = load_llm()

    print()
    print(
        "Stripe Docs Assistant is ready."
    )

    print(
        "Type 'quit' or 'exit' to stop."
    )

    print()

    while True:

        question = input("You: ").strip()


        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if question.lower() in (
            "quit",
            "exit",
        ):

            print()
            print("Goodbye!")

            break


        # ----------------------------------------------------
        # Ignore empty input
        # ----------------------------------------------------

        if not question:
            continue


        # ----------------------------------------------------
        # Run RAG
        # ----------------------------------------------------

        try:

            answer, sources = ask(
                question,
                vectorstore,
                llm,
            )


            print()
            print("Assistant:")
            print(answer)


            # ------------------------------------------------
            # Sources
            # ------------------------------------------------

            if sources:

                print()
                print("Sources:")

                for source in sources:

                    print(
                        f"  - {source}"
                    )


            print()


        except Exception as error:

            print()
            print(
                "Something went wrong while "
                "processing your question."
            )

            print(
                f"Error: {error}"
            )

            print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()