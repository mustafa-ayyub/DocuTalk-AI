"""
Handles file uploads, processing, and embedding creation for user documents.
"""

import streamlit as st
from src.services.files_processing import process_files
from src.services.text_processing import get_text_chunks
from src.services.embeddings import get_user_vectorstore


def handle_file_upload(user_id):
    """
    Manage file uploads, category assignment, and embedding creation.

    Args:
        user_id (str): Unique identifier for the user.
    """
    with st.sidebar:
        st.subheader("Your documents")
        uploaded_files = st.file_uploader(
            "Upload your files here",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            document_metadata = {}

            categories = ["Uncategorized...", "Law", "Education", "Health Care", "Business"]

            st.write("### Assign Categories")
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.write(f"**{file_name}**")
                with col2:
                    document_category = st.selectbox(
                        f"Category for {file_name}",
                        categories,
                        key=f"category_{file_name}",
                    )
                document_metadata[file_name] = document_category

            if st.button("Process"):
                with st.spinner("Processing your documents..."):
                    try:
                        raw_text = process_files(uploaded_files, document_metadata)
                        st.success("Text extraction complete ✅")
                        st.write("### Preview of Extracted Text:")
                        st.write(raw_text[:100])

                        text_chunks = get_text_chunks(raw_text)
                        st.success("Text chunking complete ✅")

                        vectorstore = get_user_vectorstore(text_chunks, user_id)
                        st.session_state.vectorstore = vectorstore
                        st.success("Embeddings creation complete ✅")
                        st.session_state.chat_enabled = True
                    except Exception as e:
                        st.error(f"Error processing files: {e}")
