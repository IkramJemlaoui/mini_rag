# src/rag_pipeline.py
# ✅ FINAL VERSION — Local Ollama + Mistral RAG pipeline

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


def build_rag(pdf_path: str):
    """
    Builds a minimal Retrieval-Augmented Generation (RAG) pipeline
    using a local Ollama model (Mistral).
    """

    print(" Loading PDF...")
    loader = PyPDFLoader("data\mon_doc.pdf")
    documents = loader.load()

    print(" Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_documents(documents)

    print(" Generating embeddings with Mistral (via Ollama)...")
    embeddings = OllamaEmbeddings(model="mistral")

    print(" Building FAISS vector store...")
    db = FAISS.from_documents(texts, embeddings)

    print(" Creating RetrievalQA pipeline with Mistral LLM...")
    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=Ollama(model="mistral"),
        retriever=retriever
    )

    print(" RAG pipeline ready!")
    return qa_chain
