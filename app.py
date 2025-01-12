"""
DocuTalk-AI Streamlit App
This app provides an AI-powered assistant to process documents 
and answer questions based on the provided text content.
"""
import streamlit as st
from dotenv import load_dotenv
from src.services.files_processing import process_files
from src.services.text_processing import get_text_chunks
from src.services.embeddings import get_vectorstore
from src.user_auth.login_form import login_form
from src.user_auth.login_form import get_welcome_message
from src.user_auth.signup_form import signup_form
from src.firebase_utils.auth_utils import logout_user

st.set_page_config(page_title="DocuTalk-AI", page_icon="📄")

# Load environment variables
load_dotenv()

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if not st.session_state.authenticated:
    st.title("Welcome to DocuTalk-AI")
    st.write("An AI-powered assistant to process your documents and answer your questions.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        login_form()

    with signup_tab:
        signup_form()
else:
    user_data = st.session_state.user_data
    username = user_data.get("username", None)
    if username:
        st.title(f"{get_welcome_message(username)}")
    else:
        st.title("Welcome, User!")
        st.warning("Your username is missing. Please contact support.")

    if st.button("Logout"):
        st.write("Logging out...")
        MESSAGE = logout_user()
        st.write(f"Session before clearing: {st.session_state}")
        
        for key in list(st.session_state.keys()):
            del st.session_state[key]
            
        st.write(f"Session after clearing: {st.session_state}")
        st.success(MESSAGE)
        st.experimental_rerun()



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

        user_question = st.text_input("Type your question here...")

        if uploaded_files and document_metadata:
            st.write("### Document Categories")
            for file_name, category in document_metadata.items():
                st.write(f"**{file_name}:** {category}")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if user_question.strip():
                st.write(f"**Your Question:** {user_question}")
            else:
                st.warning("Please enter a question.")

    if uploaded_files:
        st.subheader("Uploaded Files:")
        for file in uploaded_files:
            st.write(file.name)
    else:
        st.warning("No files uploaded.")
