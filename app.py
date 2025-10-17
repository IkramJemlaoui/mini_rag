from src.rag_pipeline import build_rag
import gradio as gr
import os
import tempfile

qa_chain = None  # Global pipeline 

def process_pdf(file):
    global qa_chain
    if not file:
        return " Please upload a PDF file first."

    tmp_path = file.name  


    print(f" Uploaded PDF saved at: {tmp_path}")
    qa_chain = build_rag(tmp_path)
    return " PDF processed successfully! You can now ask your questions below."


#  function to handle user questions
def rag_chat(question):
    if not question.strip():
        return " Please enter a valid question."
    print(f" Question: {question}")
    answer = qa_chain.run(question)
    print(f" Answer: {answer}")
    return answer

# Gradio interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="violet")) as demo:
   
    gr.HTML(
        """
        <h1 style='text-align: center; color: #c084fc;'>
         Mini RAG Chatbot with Ollama + Mistral
        </h1>
        <p style='text-align: center; color: gray;'>
        Upload one PDF on the left, then chat with it on the right.<br>
        <b>All local, all private!</b> ⚡
        </p>
        """
    )
    with gr.Row(equal_height=True):
        # Left column
        with gr.Column(scale=1, min_width=300):
            pdf_file = gr.File(label=" Upload your PDF", file_types=[".pdf"])
            upload_button = gr.Button(" Process PDF", variant="primary")
            status = gr.Textbox(
                label="Status",
                placeholder="PDF status will appear here...",
                interactive=False,
                lines=3,
            )
            upload_button.click(fn=process_pdf, inputs=pdf_file, outputs=status)  

        # Right column
        with gr.Column(scale=2, min_width=600):
            chatbot = gr.Chatbot(
                label=" Chat with your PDF",
                height=600,              
                type="messages"        
            )
            msg = gr.Textbox(
                placeholder="Type your question here",
                show_label=False,
                lines=2
            )
            send_btn = gr.Button(" Get Answer", variant="secondary")


            def chat_fn(message, history):
                if qa_chain is None:
                     return history + [
                        {"role": "assistant", "content": " Please upload and process a PDF first."}
        ]
                answer = qa_chain.invoke(message)["result"]

                # Convert both sides to new format
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": answer})

                return history

        send_btn.click(chat_fn, inputs=[msg, chatbot], outputs=chatbot)


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
