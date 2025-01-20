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

def get_user_id_by_email(email):
    """Retrieves a user ID by their email address."""
    try:
        ref = admin_db.reference("users")
        users = ref.get()
        for user_id, user_data in users.items():
            if user_data.get("email") == email:
                return user_id
        return {"error": "User not found"}
    except Exception as error:
        return {"error": str(error)} 

def save_user_data(user_id, data, partial_update=False):
    """Saves or updates user data in the database."""
    try:
        ref = admin_db.reference(f"users/{user_id}")
        if partial_update:
            ref.update(data)
        else:
            ref.set(data) 
        return {"success": True}
    except Exception as error:
        return {"error": str(error)}

def update_user_plan(user_id, plan_type):
    """Updates the user's plan type in the database."""
    try:
        ref = admin_db.reference(f"users/{user_id}/user_type")
        ref.set(plan_type)
        return {"success": True}
    except Exception as error:
        return {"error": str(error)}