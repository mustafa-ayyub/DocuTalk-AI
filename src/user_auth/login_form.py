"""
Streamlit login form for user authentication.
"""
from datetime import datetime
import streamlit as st
from src.firebase_utils.auth_utils import authenticate_user
from src.firebase_utils.db_utils import get_user_data, get_user_id_by_email

def display_login_form():
    """Displays the login form and returns user inputs."""
    st.subheader("Login to Your Account")
    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login")
    return email, password, submit

def validate_inputs(email, password):
    """Validates the login form inputs."""
    if not email or not password:
        st.warning("Email and password are required.")
        return False
    return True

def process_login(email, password):
    """Handles user authentication."""
    response = authenticate_user(email, password)
    if "error" in response:
        st.session_state.authenticated = False
        st.error(response["error"])
        return None
    return response["user"]

def fetch_and_set_user_data(user, cookie_controller):
    """Fetches and sets user data in the session state."""
    user_id = get_user_id_by_email(user["email"])
    user_data = get_user_data(user_id)
    if user_data and "error" not in user_data:
        st.session_state.authenticated = True
        st.session_state.user = user
        user_data["user_id"] = user_id
        st.session_state.user_data = user_data
        cookie_controller.set("user_id", user_id)
        st.success(f"Welcome back, {user_data.get('username', 'User')}!")
    else:
        st.error("Failed to retrieve user data. Please contact support.")

def login_form(cookie_controller):
    """Main function to handle the login workflow."""
    email, password, submit = display_login_form()

    if not submit:
        return

    if not validate_inputs(email, password):
        return

    user = process_login(email, password)
    if user:
        fetch_and_set_user_data(user, cookie_controller)

def get_welcome_message(name):
    """
    Returns a personalized welcome message based on the time of the day.

    Args:
        name (str): The name of the user.

    Returns:
        str: A welcome message.
    """
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Hello"

    return f"{greeting}, {name}!"
