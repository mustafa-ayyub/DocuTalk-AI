"""
Database operations for user data.
"""

from src.config.firebase_config import admin_db 

def save_user_data(user_id, data):
    """Saves user data to the database."""
    try:
        ref = admin_db .reference(f"users/{user_id}")
        ref.set(data)
        return {"success": True}
    except Exception as error:
        return {"error": str(error)}

def get_user_data(user_id):
    """Retrieves user data from the database."""
    try:
        ref = admin_db .reference(f"users/{user_id}")
        return ref.get()
    except Exception as error:
        return {"error": str(error)}
