"""
DocuTalk-AI Streamlit App

This app provides an AI-powered assistant to process documents 
and answer questions based on the provided text content.
"""

import streamlit as st

st.set_page_config(page_title="DocuTalk-AI", page_icon="📄")

st.title("DocuTalk-AI")
st.write("An AI-powered assistant to process your documents and answer your questions.")

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
            st.success("Files uploaded successfully!")
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
    