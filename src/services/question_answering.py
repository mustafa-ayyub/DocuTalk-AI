"""
This module handles user question answering in a Streamlit app, 
integrating vectorstore and Firebase for managing user data and chat history.
"""

import streamlit as st
from src.services.conversation_chain import answer_user_question
from src.firebase_utils.db_utils import get_user_data, save_user_data

def handle_question_answering(user_id, vectorstore, user_question):
    """
    Handles the process of answering a user's question using vectorstore and 
    maintaining rate limits and chat history.

    Args:
        user_id (str): Unique identifier for the user.
        vectorstore (object): The vectorstore used for document retrieval.
        user_question (str): The question posed by the user.
    """
    if not vectorstore:
        st.error("You need to process documents before asking questions.")
        return

    if not user_question.strip():
        st.warning("Please enter a valid question.")
        return

    user_data = get_user_data(user_id)
    if user_data.get("rate_limit", 0) <= 0:
        st.error("Your question limit has been reached. Please upgrade your plan.")
        return

    with st.spinner("Searching for answers..."):
        try:
            user_data["rate_limit"] -= 1
            save_user_data(user_id, {"rate_limit": user_data["rate_limit"]}, partial_update=True)
            st.session_state.user_data["rate_limit"] = user_data["rate_limit"]

            chat_context = "\n".join(
                [f"User: {item['question']}\nAI: {item['answer']}" for item in st.session_state.chat_history]
            )
            answer = answer_user_question(user_question, vectorstore, chat_context)

            st.session_state.chat_history.append({
                "question": user_question,
                "answer": answer
            })
        except Exception as e:
            st.error(f"An error occurred: {e}")
