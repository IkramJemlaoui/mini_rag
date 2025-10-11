# app.py
from src.rag_pipeline import build_rag
import gradio as gr

# 1️⃣ Build the RAG pipeline from your document
qa_chain = build_rag("data/mon_doc.pdf")

# 2️⃣ Define the chatbot function
def rag_chat(question):
    """Receives a question and returns the answer using the RAG pipeline"""
    return qa_chain.run(question)

# 3️⃣ Create a Gradio interface
demo = gr.Interface(
    fn=rag_chat,
    inputs="text",
    outputs="text",
    title="🧠 Mini RAG Chatbot",
    description="Pose une question sur le document PDF fourni."
)

# 4️⃣ Launch the web app
if __name__ == "__main__":
    demo.launch()
