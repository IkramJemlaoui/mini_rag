# app.py
# FINAL VERSION — uses rag_pipeline.py + local Ollama + Mistral

from src.rag_pipeline import build_rag
import gradio as gr
import os

# Ensure data path exists
PDF_PATH = "data/mon_doc.pdf"
if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f" PDF not found: {PDF_PATH}")

#  Build RAG pipeline
print(" Building the Mini RAG pipeline...")
qa_chain = build_rag(PDF_PATH)

#  Define function to handle user questions
def rag_chat(question):
    if not question.strip():
        return " Please enter a valid question."
    print(f" Question: {question}")
    answer = qa_chain.run(question)
    print(f" Answer: {answer}")
    return answer

#  Launch Gradio interface
demo = gr.Interface(
    fn=rag_chat,
    inputs="text",
    outputs="text",
    title=" Mini RAG Chatbot (Mistral via Ollama)",
    description="Pose une question sur le document PDF chargé localement."
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
