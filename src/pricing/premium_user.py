"""
Module for handling Stripe-based payment and subscription workflows, 
including session creation, pricing display, and post-payment processing.
"""

import os
import streamlit as st
import stripe
from ..firebase_utils.db_utils import update_user_plan, get_user_data, save_user_data

# Constants
PREMIUM_USER_RATE_LIMIT = 1000
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

# Initialize Stripe API key
stripe.api_key = STRIPE_API_KEY

def setup_stripe_session():
    """Create a Stripe checkout session."""
    try:
        environment = os.getenv("ENVIRONMENT", "local")
        if environment == "local":
            success_url = os.getenv("LOCAL_SUCCESS_URL")
            cancel_url = os.getenv("LOCAL_CANCEL_URL")
        else:
            success_url = os.getenv("DEPLOYED_SUCCESS_URL")
            cancel_url = os.getenv("DEPLOYED_CANCEL_URL")
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "recurring": {"interval": "month"},
                        "product_data": {
                            "name": "Premium Subscription",
                            "description": "Get unlimited access to all advanced features.",
                        },
                        "unit_amount": 1500,
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
    except Exception as e:
        st.error(f"An error occurred while creating the Stripe session: {e}")
        return None

def display_pricing_info():
    """Show pricing information and initiate payment."""
    st.title("Premium Subscription")
    st.write("Upgrade to the Premium plan and get unlimited access to advanced features for just $15 per month.")

    if st.button("Purchase Premium Plan"):
        session = setup_stripe_session()
        if session:
            st.write("Redirecting to payment...")
            st.markdown(
                f"[Click here to proceed to payment]({session.url})",
                unsafe_allow_html=True,
            )

def process_successful_payment():
    """Handle post-payment success logic."""
    st.title("Payment Successful!")
    st.write("Thank you for subscribing to the Premium plan. Your account has been upgraded.")

    user_id = get_user_id_from_session()

    if user_id:
        try:
            update_user_plan(user_id, "Premium")
            update_user_data_with_rate_limit(user_id)

            st.success("Your account is now Premium. Enjoy your benefits!")
            if st.button("Go to Home Page"):
                navigate_to_main_page()
        except Exception as e:
            st.error(f"An error occurred while updating your plan: {e}")
    else:
        handle_missing_user_id()

def get_user_id_from_session():
    """Retrieve the user ID from the session state."""
    if "user_data" in st.session_state:
        return st.session_state.user_data.get("user_id")
    else:
        st.error("Unable to verify user. Please log in again or contact support.")
        return None

def update_user_data_with_rate_limit(user_id):
    """Update user data with Premium rate limit."""
    user_data = get_user_data(user_id)
    user_data["rate_limit"] = PREMIUM_USER_RATE_LIMIT
    save_user_data(user_id, user_data, partial_update=True)

    st.session_state.user_data = user_data

def navigate_to_main_page():
    """Navigate to the main page."""
    st.session_state.current_page = "main"
    st.experimental_set_query_params(current_page="main")

def handle_missing_user_id():
    """Handle scenarios where user ID is missing in session state."""
    st.error("Session state does not contain a valid 'user_id'. Ensure it is set during login.")

def show_pricing_page():
    display_pricing_info()

def success_page():
    process_successful_payment()
