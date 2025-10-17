from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os
import hashlib
from langchain_core.retrievers import BaseRetriever      # add at top of file
from langchain.schema import Document   
from typing import List, Any
from pydantic import Field


def build_rag(pdf_path: str):
    """
    Builds a minimal RAG pipeline using a local Ollama model (Mistral).
    """

    print(" Loading PDF ")
    loader = PyPDFLoader("data\mon_doc.pdf")
    documents = loader.load()
    

    print("Text splitting into chunks")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    texts = splitter.split_documents(documents)
  
    # Hashing the file to detect changes
    with open(pdf_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    


    print(" Generating embeddings with nomic-embed-text model")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    persist_dir = f"vector_store_{file_hash[:8]}"
    
    # Load existing or create new Chroma store
    if os.path.exists(persist_dir):
        print(f" Loading existing Chroma vector store for {pdf_path}")
        db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("Building new Chroma vector store (first run for this PDF)")
        db = Chroma.from_documents(texts, embeddings, persist_directory=persist_dir)
        db.persist()
        print("Chroma vector store saved for future runs")

    # ✅ --- NEW CODE STARTS HERE ---
    class ThresholdRetriever(BaseRetriever):
        """Custom retriever with similarity threshold filtering."""

        db: Any = Field(...)
        threshold: float = Field(default=0.35)

        def _get_relevant_documents(self, query: str) -> List[Document]:
            results = self.db.similarity_search_with_score(query, k=5)
            filtered_docs = []
            for doc, score in results:
                if score >= self.threshold:
                    print(f"✅ Keeping chunk (score={score:.3f}): {doc.page_content[:100]}...")
                    filtered_docs.append(doc)
                else:
                    print(f"❌ Ignoring chunk (score={score:.3f}) — below threshold.")
            return filtered_docs

        async def _aget_relevant_documents(self, query: str) -> List[Document]:
            """Async version required by LangChain — calls sync method."""
            return self._get_relevant_documents(query)
    retriever = ThresholdRetriever(db=db, threshold=0.35)   

# ✅ --- NEW CODE ENDS HERE ---

    print("🤖 Creating RetrievalQA pipeline with Mistral LLM...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=Ollama(model="mistral"),
        retriever=retriever
    )


    print(" RAG pipeline ready!")
    return qa_chain
