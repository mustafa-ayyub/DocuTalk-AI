"""
Firebase configuration and initialization.
"""

import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
import pyrebase

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(
        cred, {"databaseURL": os.getenv("FIREBASE_DATABASE_URL")}
    )

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

admin_db = db
