"""
Stripe Docs RAG Assistant - Build Vector Store
------------------------------------------------
Loads the markdown files downloaded by ingest_docs.py, splits them into
overlapping chunks, embeds each chunk with Gemini's embedding model, and
persists everything into a local Chroma vector database.

Run this once after ingest_docs.py (and again any time data/raw/ changes).
"""

import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()  # reads GOOGLE_API_KEY from .env

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "GOOGLE_API_KEY not found or still set to the placeholder value. "
        "Open your .env file and paste your real Gemini API key after "
        "GOOGLE_API_KEY= (no quotes, no spaces)."
    )

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# Chunking config - deliberately chosen and worth explaining in interviews:
# - 800 chars keeps each chunk focused on one concept/section rather than
#   mixing multiple topics, which improves retrieval precision.
# - 150 char overlap prevents losing context at chunk boundaries (e.g. a
#   sentence that explains a term right before it's used).
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def load_documents():
    loader = DirectoryLoader(
        RAW_DATA_DIR,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} raw documents.")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks


def build_vectorstore(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    print("Embedding chunks and building Chroma vector store... "
          "(batched to respect the free tier rate limit, may take a couple minutes)")

    # Free tier allows a limited number of embedding requests/minute, so we
    # batch small and pause between batches rather than firing all at once.
    BATCH_SIZE = 10
    PAUSE_SECONDS = 15

    vectorstore = Chroma(
        collection_name="stripe_docs",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )

    total = len(chunks)
    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        added = False
        attempts = 0

        while not added and attempts < 3:
            try:
                vectorstore.add_documents(batch)
                added = True
                print(f"  Embedded {min(i + BATCH_SIZE, total)}/{total} chunks")
            except Exception as e:
                attempts += 1
                wait = 30 * attempts
                print(f"  Rate limit or error hit, retrying in {wait}s... ({e})")
                time.sleep(wait)

        if i + BATCH_SIZE < total:
            time.sleep(PAUSE_SECONDS)

    print(f"Vector store built and saved to: {PERSIST_DIR}")
    return vectorstore


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    build_vectorstore(chunks)