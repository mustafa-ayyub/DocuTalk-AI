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
        "Upload your files here",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        document_metadata = {}  # Dictionary to store file name and category

        categories = ["Uncatogerized", "Law", "Education", "Health Care", "Business"]


        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name

            # Ask for category for each document
            document_category = st.selectbox(
                f"Category for {file_name}",
                categories,
                key=f"category_{file_name}"  
            )
             
            document_metadata[file_name] = document_category

        st.write("### Document Metadata")
        st.json(document_metadata)

        if st.button("Process"):
            with st.spinner("Processing your documents..."):
                # Simulate document processing
                raw_text = process_files(uploaded_files)
                st.success("Step 1: Text extraction complete ✅")
                preview_text = raw_text[:100]

                st.subheader("Preview of the Extracted Text:")
                st.write(preview_text)

                text_chunks = get_text_chunks(raw_text)
                st.success("Step 2: Text chunking complete ✅")

                vectorstore = get_vectorstore(text_chunks)
                st.success("Step 3: Embeddings creation complete ✅")


with st.form("chat-form", clear_on_submit=True):
    
    st.subheader("Ask a question about your documents")

    # Input field for user question
    user_question = st.text_input("Type your question here...")

    # Display categories for uploaded documents
    if uploaded_files and document_metadata:
        st.write("### Document Categories")
        for file_name, category in document_metadata.items():
            st.write(f"**{file_name}:** {category}")

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