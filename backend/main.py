from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware



# Allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"] if your frontend runs there
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # allow all headers
)


# Load API key from environment
client = Groq(api_key=os.getenv("API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Groq Chatbot API is running. Use POST /chat."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": request.message}
        ],
    )
    # Correct attribute access
    reply = response.choices[0].message.content
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
