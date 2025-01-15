"""
DocuTalk-AI Streamlit App
This app provides an AI-powered assistant to process documents 
and answer questions based on the provided text content.
"""

import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController
from src.user_auth.authentication import handle_authentication
from src.user_auth.login_form import get_welcome_message
from src.user_auth.user_type_handling import show_user_type_content
from src.services.file_upload_handler import handle_file_upload
from src.services.question_answering import handle_question_answering
from src.pricing.premium_user import show_pricing_page, success_page
from src.firebase_utils.auth_utils import logout_user, check_authentication

st.set_page_config(page_title="DocuTalk-AI", page_icon="📄")

load_dotenv()
cookie_controller = CookieController()
check_authentication(cookie_controller)

authenticated = handle_authentication(cookie_controller)

if not authenticated:
    st.stop()

query_params = st.experimental_get_query_params()
if "current_page" in query_params:
    st.session_state.current_page = query_params["current_page"][0]

if st.session_state.current_page == "pricing":
    show_pricing_page()
    st.stop()

if st.session_state.current_page == "success":
    success_page()
    st.stop()

with st.sidebar:
    if st.button("Logout", key="logout_button"):
        logout_user(cookie_controller)

user_data = st.session_state.user_data
username = user_data.get("username", "User")
user_id = user_data.get("user_id", "Unknown")
rate_limit = user_data.get("rate_limit", 0)
user_type = user_data.get("user_type", "Basic")

st.title(f"{get_welcome_message(username)}!")

st.subheader("Your Plan Details")
col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"**Plan:** {user_type}")
    st.write(f"**Remaining Questions:** {rate_limit}")
with col2:
    if user_type == "Basic":
        if st.button("Go Pro"):
            st.session_state.current_page = "pricing"
            st.experimental_rerun()

handle_file_upload(user_id)

st.subheader("Ask a question about your documents")

with st.form("chat-form", clear_on_submit=True):
    user_question = st.text_input(
        "Type your question here...",
        value=st.session_state.user_question,
        disabled=not st.session_state.chat_enabled,
        placeholder="Upload and process a file to enable this field.",
    )
    submit_button = st.form_submit_button("Submit")

    if submit_button and user_question.strip():
        if st.session_state.chat_enabled:
            vectorstore = st.session_state.get("vectorstore", None)
            handle_question_answering(user_id, vectorstore, user_question)

            st.session_state.user_question = ""
        else:
            st.warning("Please upload and process a file before asking questions.")

if st.session_state.chat_history:
    st.subheader("Chat History")
    for chat in reversed(st.session_state.chat_history):
        st.write(f"**Q:** {chat['question']}")
        st.write(f"**A:** {chat['answer']}\n")

