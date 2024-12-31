"""
Authentication module for user operations.
"""

import streamlit as st
from src.config.firebase_config import auth


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


def logout_user():
    """Logs out the current user."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_data = {}
    st.session_state.signup_completed = False
    return "You have been logged out successfully."
