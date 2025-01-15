"""
Manages user authentication for the DocuTalk-AI app.
"""

import streamlit as st
from src.user_auth.login_form import login_form
from src.user_auth.signup_form import signup_form
from src.firebase_utils.auth_utils import logout_user, check_authentication

def handle_authentication(cookie_controller):
    """
    Checks user authentication and shows login or signup forms if needed.

    Args:
        cookie_controller (object): Manages authentication cookies.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    check_authentication(cookie_controller)

    if not st.session_state.authenticated:
        st.title("Welcome to DocuTalk-AI")
        st.write("AI assistant for document processing and Q&A.")

        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            login_form(cookie_controller)

        with signup_tab:
            signup_form()
        return False
    return True
