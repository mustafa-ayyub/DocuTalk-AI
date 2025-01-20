"""
Displays content based on the user's subscription type.
"""

import streamlit as st

def show_user_type_content(user_data):
    """
    Displays features and options based on the user's subscription type.

    Args:
        user_data (dict): Information about the user, including subscription type.
    """
    user_type = user_data.get("user_type", "Basic")

    if user_type == "Premium":
        st.success("🎉 You are a Pro User! Enjoy premium features.")
        with st.expander("Your Premium Benefits"):
            st.write("""
            - Upto 1000 question answering
            - Access to advanced AI-powered features
            - Priority customer support
            - Exclusive updates and tools
            """)
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Upgrade to unlock unlimited access to premium features.")
        with col2:
            if st.button("Go Pro"):
                st.session_state.current_page = "pricing"
                st.experimental_rerun()
