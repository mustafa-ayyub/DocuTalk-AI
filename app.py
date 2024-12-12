"""
DocuTalk-AI Streamlit App

This app provides an AI-powered assistant to process documents 
and answer questions based on the provided text content.
"""

import streamlit as st
from src.services.files_processing import process_files
from src.services.text_processing import get_text_chunks
from src.services.embeddings import get_vectorstore
from dotenv import load_dotenv

st.set_page_config(page_title="DocuTalk-AI", page_icon="📄")

st.title("DocuTalk-AI")
st.write("An AI-powered assistant to process your documents and answer your questions.")

load_dotenv()
# Sidebar for file upload
with st.sidebar:
    st.subheader("Your documents")
    uploaded_files = st.file_uploader(
        "Upload your files here and click on 'Process'",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if st.button("Process"):
        if uploaded_files:
            with st.spinner("Processing your documents..."):
                raw_text = process_files(uploaded_files)
                preview_text = raw_text[:100]

                st.success("Step 1: Text extraction complete ✅")
                st.subheader("Preview of the Extracted Text:")
                st.write(preview_text)

                text_chunks = get_text_chunks(raw_text)
                text_chunks_preview = text_chunks[0][:150]
                st.success("Step 2: Text chunking complete ✅")
                st.write(text_chunks_preview)

                vectorstore = get_vectorstore(text_chunks)
                st.success("Step 3: Embeddings creation complete ✅")


        else:
            st.warning("Please upload files to process.")

with st.form("chat-form", clear_on_submit=True):
    st.subheader("Ask a question about your documents")

    # Input field for user question
    user_question = st.text_input("Type your question here...")

    # Submit button for the form
    submit_button = st.form_submit_button("Submit")

    # If the submit button is pressed, display the input question
    if submit_button:
        if user_question.strip():
            st.write(f"**Your Question:** {user_question}")
        else:
            st.warning("Please enter a question.")

# Show uploaded file names if any files are uploaded
if uploaded_files:
    st.subheader("Uploaded Files:")
    for file in uploaded_files:
        st.write(file.name)
else:
    st.warning("No files uploaded.")
    