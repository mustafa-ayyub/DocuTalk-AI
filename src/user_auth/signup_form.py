"""
Streamlit signup form for user registration.
"""

import streamlit as st
from src.firebase_utils.auth_utils import register_user
from src.firebase_utils.db_utils import save_user_data

def display_signup_form():
    """Displays the signup form and returns user inputs."""
    st.subheader("Create a New Account")
    with st.form("signup_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Enter your username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter a strong password")
        submit = st.form_submit_button("Sign Up")
    return username, email, password, submit

def validate_signup_inputs(username, email, password):
    """Validates the signup form inputs."""
    if not (username and email and password):
        st.warning("All fields are required.")
        return False
    if "@" not in email or len(password) < 6:
        st.warning("Please ensure email is valid and password is at least 6 characters long.")
        return False
    return True

def register_new_user(email, password):
    """Registers a new user."""
    response = register_user(email, password)
    if "error" in response:
        st.session_state.authenticated = False
        st.error(response["error"])
        return None
    return response["user"]

def save_and_set_user_data(user_id, username, email):
    """Saves user data to the database and updates session state."""
    user_data = {
        "username": username,
        "email": email,
        "rate_limit": 60,
        "user_type": "Basic",
    }
    db_response = save_user_data(user_id, user_data)

    if "error" in db_response:
        st.error("Error saving user details to the database.")
        return False

    st.session_state.authenticated = True
    st.session_state.user_data = user_data
    st.success("User details saved successfully!")
    return True

def signup_form():
    """Main function to handle the signup workflow."""
    username, email, password, submit = display_signup_form()

    if not submit:
        return

    if not validate_signup_inputs(username, email, password):
        return

    user = register_new_user(email, password)
    if user:
        user_id = user["localId"]
        if save_and_set_user_data(user_id, username, email):
            st.experimental_rerun()
