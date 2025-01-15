"""
Authentication module for user operations.
"""

import streamlit as st
from src.config.firebase_config import auth
from streamlit_cookies_controller import CookieController
from .db_utils import get_user_data



def authenticate_user(email, password):
    """Authenticates a user with email and password."""
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return {"user": user}
    except Exception:
        return {"error": "Invalid email or password. Please try again."}


def register_user(email, password):
    """Registers a new user with email and password."""
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return {"user": user}
    except Exception:
        return {"error": "An unexpected error occurred. Please try again later."}

def logout_user(cookie_controller):
    """Logs out the current user."""
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.session_state.current_page = "main"

    cookie_controller.set("user_id", "", max_age=0)

    st.success("Logged out successfully!")
    
def check_authentication(cookie_controller):
    "Initializes session variables and checks user authentication status using cookies. Updates session state based on user data."
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_data = {}

    if "current_page" not in st.session_state:
        st.session_state.current_page = "main"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""
    
    if "chat_enabled" not in st.session_state:
        st.session_state.chat_enabled = False

    user_id = cookie_controller.get("user_id")
    if user_id:
        st.session_state.authenticated = True
        user_data = get_user_data(user_id)
        user_data["user_id"] = user_id
        st.session_state.user_data = user_data
    else:
        st.session_state.authenticated = False
        st.session_state.user_data = {}