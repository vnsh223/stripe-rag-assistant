"""
Stripe Docs RAG Assistant - Build Vector Store
------------------------------------------------
Loads the markdown files downloaded by ingest_docs.py, splits them into
overlapping chunks, embeds each chunk using a local Hugging Face
Sentence Transformer model, and persists everything into Chroma.

Run this once after ingest_docs.py (and again any time data/raw/ changes,
or any time you switch embedding models - old embeddings are NOT
compatible with a new embedding model, so this always rebuilds fresh).
"""

import os
import shutil

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


RAW_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw"
)

PERSIST_DIR = os.path.join(
    os.path.dirname(__file__), "..", "chroma_db"
)

COLLECTION_NAME = "stripe_docs"

# Chunking configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def load_documents():
    """Load all Markdown documents from data/raw."""
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
    """Split documents into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks


def build_vectorstore(chunks):
    """Create embeddings locally and store them in a FRESH Chroma store.

    Always wipes any existing chroma_db first. This matters whenever the
    embedding model changes (e.g. Gemini -> Hugging Face) - vectors from
    a different embedding model are not compatible with each other and
    silently produce a broken/mismatched collection if mixed.
    """
    if os.path.exists(PERSIST_DIR):
        print(f"Removing old vector store at {PERSIST_DIR} ...")
        shutil.rmtree(PERSIST_DIR)

    print("Loading Hugging Face embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding chunks and building Chroma vector store...")
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    vectorstore.add_documents(chunks)

    # Verify the data actually landed - this is what was silently missing
    # before, causing the deployed app's "collection not found" error.
    count = vectorstore._collection.count()
    print(f"Vector store built at: {PERSIST_DIR}")
    print(f"Collection '{COLLECTION_NAME}' now contains {count} chunks.")

    if count == 0:
        raise RuntimeError(
            "Vector store was created but contains 0 chunks - "
            "something went wrong during embedding. Check the logs above."
        )

    return vectorstore


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    build_vectorstore(chunks)