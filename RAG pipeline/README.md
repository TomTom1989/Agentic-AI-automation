# RAG Pipeline with Vector Visualization & Chatbot

This project implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain and OpenAI, featuring vector embedding storage in ChromaDB, interactive chatbot interface with Gradio, and 2D/3D vector visualizations via Plotly and t-SNE.

## Features
- Load and split Markdown documents from multiple folders
- Generate OpenAI embeddings and store in Chroma vector database
- Visualize embeddings in 2D & 3D with Plotly (t-SNE)
- Chatbot with memory using Gradio + LangChain ConversationalRetrievalChain

## Tech Stack
- **Python**, **LangChain**, **OpenAI GPT-4o Mini**
- **Chroma** for persistent vector storage
- **Gradio** for the interactive chatbot
- **Plotly + scikit-learn (t-SNE)** for dimensionality reduction and visualization
- **dotenv** for secure API key management

## Folder Structure
- `knowledge-base/` — Markdown files grouped by topic for embedding
- `vector_db/` — Persisted Chroma vectorstore (auto-created)