"""
Stripe Docs RAG Assistant - RAG Chain
----------------------------------------
The core retrieval + generation pipeline:
  1. Take a user question
  2. Retrieve the most relevant chunks from the Chroma vector store
  3. Feed those chunks + the question to Gemini
  4. Return a grounded answer with source citations, or a clear
     "not found in the docs" fallback instead of hallucinating

Run this file directly for a quick terminal test loop before wiring it
into the Streamlit UI.
"""

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "GOOGLE_API_KEY not found or still set to the placeholder value. "
        "Check your .env file."
    )

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# How many chunks to retrieve per question. 4 gives enough context to
# answer most questions without overwhelming the prompt with noise.
TOP_K = 4

# The system prompt is deliberately strict about grounding: it must refuse
# to answer from general knowledge if the docs don't cover it, which is
# the key thing that separates a real RAG system from "ChatGPT with extra
# steps" - and a good thing to point out in an interview.
SYSTEM_PROMPT = """You are a support assistant that answers questions using \
ONLY the Stripe documentation excerpts provided below. You are not allowed \
to use any outside knowledge about Stripe or payments in general.

Rules:
- If the answer is fully or partially contained in the excerpts, answer \
clearly and concisely, and mention which excerpt(s) you used.
- If the excerpts do NOT contain enough information to answer the \
question, say plainly: "I couldn't find this in the Stripe docs I have \
access to." Do not guess or fill gaps with general knowledge.
- Keep answers focused and practical, as if helping a support agent or \
developer quickly.

Documentation excerpts:
{context}
"""


def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )
    return Chroma(
        collection_name="stripe_docs",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )


def format_context(docs):
    """Turn retrieved chunks into a numbered, source-labeled context block."""
    blocks = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown source")
        blocks.append(f"[Excerpt {i} - Source: {source}]\n{doc.page_content}")
    return "\n\n".join(blocks)

def retrieve_with_retry(retriever, question, max_attempts=4):
    """Retry retrieval with backoff - the free tier rate limit can be hit
    on query embeddings too, not just during the initial bulk ingest."""
    attempt = 0
    while True:
        try:
            return retriever.invoke(question)
        except Exception as e:
            attempt += 1
            if attempt >= max_attempts:
                raise
            wait = 15 * attempt
            print(f"  (Rate limited, retrying in {wait}s...)")
            time.sleep(wait)


def ask(question: str, vectorstore, llm):
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    docs = retrieve_with_retry(retriever, question)

    if not docs:
        return "I couldn't find this in the Stripe docs I have access to.", []

    context = format_context(docs)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})

    sources = sorted(set(doc.metadata.get("source", "unknown") for doc in docs))
    return response.content, sources


def main():
    vectorstore = load_vectorstore()
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-3.6-flash",  # fast + free-tier friendly; if this model
        # is ever retired, check https://ai.google.dev/gemini-api/docs/models
        # for the current "flash" tier model name and swap it in here
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,  # low temperature keeps answers grounded, not creative
    )

    print("Stripe Docs Assistant ready. Type a question (or 'quit' to exit).\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        answer, sources = ask(question, vectorstore, llm)
        print(f"\nAssistant: {answer}")
        if sources:
            print("\nSources:")
            for s in sources:
                print(f"  - {s}")
        print()


if __name__ == "__main__":
    main()