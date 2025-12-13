import os
import sqlite3
import hashlib
import logging
from datetime import datetime
import json
from fastapi import FastAPI

app = FastAPI()


# configure logging for DB diagnostics
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database path (absolute, repo-relative)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "chatbot.db")

class DatabaseManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def get_db_connection():
        # Use an absolute path and enable foreign keys for each connection
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON")
        except Exception:
            # Non-fatal: log and continue
            logger.exception("Failed to enable foreign keys for SQLite connection")
        return conn

    # User Management
    @staticmethod
    def register_user(username: str, email: str, password: str, first_name: str, last_name: str):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            hashed_password = DatabaseManager.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, hashed_password, first_name, last_name))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {"success": True, "user_id": user_id, "message": "User registered successfully"}
        except sqlite3.IntegrityError as e:
            logger.warning("Register integrity error: %s", e)
            return {"success": False, "message": "Username or email already exists"}
        except Exception as e:
            logger.exception("register_user failed")
            return {"success": False, "message": str(e)}

    @staticmethod
    def login_user(email: str, password: str):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            hashed_password = DatabaseManager.hash_password(password)
            
            cursor.execute("""
                SELECT user_id, username, first_name, email FROM users 
                WHERE email = ? AND password = ?
            """, (email, hashed_password))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "success": True,
                    "user_id": result[0],
                    "username": result[1],
                    "first_name": result[2],
                    "email": result[3],
                    "message": "Login successful"
                }
            else:
                return {"success": False, "message": "Invalid email or password"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_user(user_id: int):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, email, first_name, last_name, created_at 
                FROM users WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "success": True,
                    "user_id": result[0],
                    "username": result[1],
                    "email": result[2],
                    "first_name": result[3],
                    "last_name": result[4],
                    "created_at": result[5]
                }
            else:
                return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Session Management
    @staticmethod
    def start_session(user_id: int):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO sessions (user_id) VALUES (?)", (user_id,))
            conn.commit()
            session_id = cursor.lastrowid
            conn.close()
            
            return {"success": True, "session_id": session_id}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def end_session(session_id: int):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE sessions SET ended_at = ? WHERE session_id = ?
            """, (datetime.now(), session_id))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "Session ended"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # Message Management
    @staticmethod
    def save_message(session_id: int, user_id: int, sender: str, message: str, language: str = "en"):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()

            # Validate user exists
            cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone() is None:
                return {"success": False, "message": f"User {user_id} does not exist"}

            # Validate session exists
            cursor.execute("SELECT 1 FROM sessions WHERE session_id = ?", (session_id,))
            if cursor.fetchone() is None:
                return {"success": False, "message": f"Session {session_id} does not exist"}

            # Insert message
            cursor.execute("""
                INSERT INTO messages (session_id, user_id, sender, message, language)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, user_id, sender, message, language))

            conn.commit()
            message_id = cursor.lastrowid
            conn.close()

            return {"success": True, "message_id": message_id}
        except Exception as e:
            logger.exception("save_message failed")
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_chat_history(session_id: int):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT sender, message, language, created_at FROM messages 
                WHERE session_id = ? 
                ORDER BY created_at
            """, (session_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "sender": row[0],
                    "message": row[1],
                    "language": row[2],
                    "created_at": row[3]
                })
            
            conn.close()
            return {"success": True, "messages": messages}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_user_chat_history(user_id: int):
        try:
            conn = DatabaseManager.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT m.sender, m.message, m.language, m.created_at, s.session_id
                FROM messages m
                JOIN sessions s ON m.session_id = s.session_id
                WHERE m.user_id = ?
                ORDER BY m.created_at DESC
            """, (user_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "sender": row[0],
                    "message": row[1],
                    "language": row[2],
                    "created_at": row[3],
                    "session_id": row[4]
                })
            
            conn.close()
            return {"success": True, "messages": messages}
        except Exception as e:
            return {"success": False, "message": str(e)}

# Initialize database
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database Manager loaded successfully!")
    print("Available methods:")
    print("  - register_user(username, email, password, first_name, last_name)")
    print("  - login_user(email, password)")
    print("  - get_user(user_id)")
    print("  - start_session(user_id)")
    print("  - end_session(session_id)")
    print("  - save_message(session_id, user_id, sender, message, language)")
    print("  - get_chat_history(session_id)")
    print("  - get_user_chat_history(user_id)")
