# 🤖 Mini RAG Chatbot – Local AI Assistant

> **An intelligent local assistant that answers questions from PDF documents using a Retrieval-Augmented Generation (RAG) architecture.**  
> Built with **LangChain**, **Ollama (Mistral)**, **ChromaDB**, and **Gradio**.

---

## 🎯 Project Goal

Créer un **assistant intelligent local** capable de répondre à des questions en langage naturel à partir d’un document PDF.  
Le projet met en œuvre une architecture **Retrieval-Augmented Generation (RAG)** pour combiner **recherche sémantique** et **génération de texte**, garantissant des **réponses précises, pertinentes et contextuelles**.

---

## 🧩 Tech Stack

| Category | Tools / Frameworks |
|-----------|--------------------|
| **Langage** | Python |
| **Framework RAG** | LangChain |
| **LLM Local** | Ollama (Mistral) |
| **Vector Store** | ChromaDB |
| **Interface Web** | Gradio |
| **Conteneurisation** | Docker |
| **Embeddings** | nomic-embed-text |
| **Alternative Vector Store** | FAISS |

---

## 🏗️ Architecture Overview

**Pipeline RAG complet :**

1. 📥 Chargement et découpage du PDF  
2. 🧮 Génération d’embeddings via *nomic-embed-text*  
3. 🧠 Stockage et recherche sémantique avec *ChromaDB*  
4. 💬 Génération de réponses par *Mistral* (via Ollama)  
5. 🌐 Interface utilisateur simple et interactive avec *Gradio*  

```text
User Query → PDF Splitter → Embeddings → Vector Store → RAG Chain → Answer
