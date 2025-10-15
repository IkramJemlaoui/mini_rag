from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os
import hashlib



def build_rag(pdf_path: str):
    """
    Builds a minimal Retrieval-Augmented Generation (RAG) pipeline
    using a local Ollama model (Mistral).
    """

    print(" Loading PDF...")
    loader = PyPDFLoader("data\mon_doc.pdf")
    documents = loader.load()
    

    print(" Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = splitter.split_documents(documents)
  
    # Compute a hash of the file to identify if it changed
    with open(pdf_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    # Each unique PDF has its own vector store folder
    persist_dir = f"vector_store_{file_hash[:8]}"


    print(" Generating embeddings with nomic-embed-text (via Ollama)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    persist_dir = "vector_store"
    
    # NEW SECTION — caching logic (load existing or create new Chroma store)
    if os.path.exists(persist_dir):
        print(f"🔄 Loading existing Chroma vector store for {pdf_path}...")
        db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("💾 Building new Chroma vector store (first run for this PDF)...")
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_dir)
        db.persist()
        print("✅ Chroma vector store saved for future runs!")

    print("🤖 Creating RetrievalQA pipeline with Mistral LLM...")
    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=Ollama(model="mistral"),
        retriever=retriever
    )

    print(" RAG pipeline ready!")
    return qa_chain
