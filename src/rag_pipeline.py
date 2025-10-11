# src/rag_pipeline.py
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama



def build_rag(pdf_path: str):
    """
    Builds a minimal Retrieval-Augmented Generation (RAG) pipeline
    from one PDF document.
    """

    # 1️⃣ Load the document
    loader = PyPDFLoader("C:/Users/Ikram/Downloads/RAG_PDF.pdf")
    documents = loader.load()

    # 2️⃣ Split the text into small chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_documents(documents)

    # 3️⃣ Create embeddings and vector index
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    # 4️⃣ Build Retrieval + LLM chain
    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=Ollama(model="mistral"),
         retriever=retriever
    )

    return qa_chain
