# 💳 Stripe Docs AI

> An AI-powered documentation assistant that answers Stripe-related questions using Retrieval-Augmented Generation (RAG) and only the Stripe documentation stored in its knowledge base.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://www.langchain.com/)
[![Chroma](https://img.shields.io/badge/Vector%20DB-Chroma-orange)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/Embeddings-Hugging%20Face-yellow?logo=huggingface)](https://huggingface.co/)
[![Groq](https://img.shields.io/badge/LLM-Groq-purple)](https://groq.com/)

---

## 🚀 Live Demo

🔗 **Live Application:**  
https://stripe-rag-assistant.streamlit.app/

> The application allows users to ask questions about Stripe documentation and receive grounded answers with source references.

---

## 📌 Overview

Stripe provides extensive documentation covering payments, webhooks, APIs, authentication, subscriptions, and many other concepts.

Finding the correct information across large documentation sets can be time-consuming.

**Stripe Docs AI** solves this problem by providing a conversational interface where users can ask questions in natural language.

Instead of asking an LLM to answer directly from its general knowledge, the application first retrieves relevant Stripe documentation and then provides that context to the language model.

This approach is known as:

**Retrieval-Augmented Generation (RAG).**

---

# 🎯 Problem Statement

Large Language Models can generate useful answers, but they have an important limitation:

> They may generate information that is not present in the source documentation.

This is especially problematic when building documentation assistants because incorrect technical information can mislead developers.

The goal of this project is to build an AI assistant that:

- Retrieves relevant Stripe documentation
- Generates answers using retrieved documentation
- Avoids relying on external knowledge
- Provides source URLs
- Rejects questions outside the available knowledge base
- Maintains conversation history in the user interface

---

# 💡 Solution

The application implements a RAG pipeline.

The workflow is:

```text
Stripe Documentation
        ↓
Document Loading
        ↓
Text Chunking
        ↓
Hugging Face Embeddings
        ↓
Chroma Vector Database
        ↓
User Question
        ↓
Similarity Search
        ↓
Relevant Documentation
        ↓
Groq LLM
        ↓
Grounded Answer
        ↓
Source URLs
