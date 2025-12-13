from fastapi import FastAPI, HTTPException
import os
import runpy
import logging
import sqlite3

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app import DatabaseManager
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("API_KEY") or os.getenv("api_key"))

# Ensure the SQLite database exists and is initialized
def ensure_db():
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        db_path = os.path.join(base_dir, "database", "chatbot.db")
        init_script = os.path.join(base_dir, "database", "chatbot_db.py")
        
        needs_init = False
        if not os.path.exists(db_path):
            needs_init = True
        else:
            # DB file exists, check if it has the tables
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                # Check for all required tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'sessions', 'messages')")
                tables_found = {row[0] for row in cursor.fetchall()}
                conn.close()
                if len(tables_found) < 3:
                    needs_init = True
            except Exception as e:
                logging.error(f"DB check failed, re-initializing. Error: {e}")
                needs_init = True

        if needs_init:
            # run the initializer script to create the DB and tables
            print(f"Database is missing or incomplete. Initializing at {db_path}...")
            if os.path.exists(init_script):
                runpy.run_path(init_script, run_name="__main__")
                print("Database initialized successfully.")
            else:
                logging.error(f"Initializer script not found at {init_script}")
        else:
            # DB exists and contains tables
            print(f"Database already exists and is valid at {db_path}")
    except Exception as e:
        # Log but don't stop the server startup
        logging.exception("Failed to ensure DB initialized: %s", e)

# Run ensure_db at import/startup so the DB file is present when the server runs
ensure_db()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatMessage(BaseModel):
    session_id: int
    user_id: int
    message: str
    language: str = "en"

class MessageToSave(BaseModel):
    session_id: int
    user_id: int
    sender: str
    message: str
    language: str = "en"

# Registration endpoint
@app.post("/register")
def register(user: UserRegister):
    result = DatabaseManager.register_user(
        user.username,
        user.email,
        user.password,
        user.first_name,
        user.last_name
    )
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# Login endpoint
@app.post("/login")
def login(user: UserLogin):
    result = DatabaseManager.login_user(user.email, user.password)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=401, detail=result["message"])

# Get user info
@app.get("/user/{user_id}")
def get_user(user_id: int):
    result = DatabaseManager.get_user(user_id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=404, detail=result["message"])

# Start new session
@app.post("/start_session")
def start_session(user_id: int):
    result = DatabaseManager.start_session(user_id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# End session
@app.post("/end_session/{session_id}")
def end_session(session_id: int):
    result = DatabaseManager.end_session(session_id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# Save message to database
@app.post("/save_message")
def save_message(msg: MessageToSave):
    print(f"DEBUG: Received save_message request: session_id={msg.session_id}, user_id={msg.user_id}, sender={msg.sender}, message={msg.message[:50]}...")
    result = DatabaseManager.save_message(
        msg.session_id,
        msg.user_id,
        msg.sender,
        msg.message,
        msg.language
    )
    if result["success"]:
        return result
    else:
        print(f"DEBUG: save_message failed: {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])

# Get chat history for a session
@app.get("/chat_history/{session_id}")
def get_chat_history(session_id: int):
    result = DatabaseManager.get_chat_history(session_id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# Get all chat history for a user
@app.get("/user_chat_history/{user_id}")
def get_user_chat_history(user_id: int):
    result = DatabaseManager.get_user_chat_history(user_id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# Chat endpoint that integrates with Groq
@app.post("/chat")
def chat(chat_msg: ChatMessage):
    """
    Save user message and return bot response
    """
    # Save user message
    save_result = DatabaseManager.save_message(
        chat_msg.session_id,
        chat_msg.user_id,
        'user',
        chat_msg.message,
        chat_msg.language
    )
    
    if not save_result["success"]:
        raise HTTPException(status_code=400, detail="Failed to save message")
    
    # Call Groq API to get response
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": chat_msg.message}
            ],
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Groq API error: {e}")
        bot_response = "Sorry, I'm having trouble connecting to my brain right now. Please try again later."
    
    # Save bot response
    bot_save_result = DatabaseManager.save_message(
        chat_msg.session_id,
        chat_msg.user_id,
        'bot',
        bot_response,
        chat_msg.language
    )
    
    return {"success": True, "reply": bot_response, "message_id": bot_save_result.get("message_id")}

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend is running"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Chatbot API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
