# HealthBot AI

AI-powered health assistant providing general health information and guidance.

## Tech Stack

- **Frontend:** React + Vite + TypeScript + Tailwind CSS
- **Backend:** Python + FastAPI + SQLAlchemy
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **AI:** Groq (Llama 3.1)
- **Auth:** JWT + bcrypt

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
cp .env.example .env         # Add your GROQ_API_KEY
python main.py
```

Backend runs at http://localhost:8001

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## Environment Variables

Copy `.env.example` to `backend/.env` and fill in:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (get from console.groq.com) |
| `SECRET_KEY` | Random string for JWT signing |
| `DATABASE_URL` | Database connection string |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/chat` | Send chat message |
| GET | `/api/conversations` | List conversations |
| POST | `/api/conversations` | Create conversation |
| DELETE | `/api/conversations/{id}` | Delete conversation |
| POST | `/api/symptoms/check` | Symptom checker |
| GET | `/api/health-profile` | Get health profile |
| PUT | `/api/health-profile` | Update health profile |
| POST | `/api/documents/upload` | Upload document |
| GET | `/api/documents` | List documents |
| POST | `/api/reports/generate/{id}` | Generate report |
| GET | `/api/settings` | Get settings |
| PUT | `/api/settings` | Update settings |

## Project Structure

```
infosys-project/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt
│   ├── app/
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # DB setup
│   │   ├── core/security.py    # Auth & JWT
│   │   ├── models/             # SQLAlchemy + Pydantic
│   │   ├── routers/            # API endpoints
│   │   ├── services/           # Business logic
│   │   └── prompts/            # AI prompts
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── api/                # API clients
│   │   ├── components/         # React components
│   │   ├── context/            # React contexts
│   │   ├── hooks/              # Custom hooks
│   │   └── pages/              # Page components
│   └── ...
└── README.md
```

## Features

- AI Health Chat with conversation context
- Symptom Checker with structured flow
- Emergency detection system
- Health document upload & analysis
- Health profile management
- Conversation history with search
- Voice input support
- Dark/light theme
- Responsive design
- Rate limiting & input sanitization

## Safety

- Never claims to diagnose
- Emergency detection system
- AI safety layer filters dangerous advice
- All responses include medical disclaimers
- Prompt injection detection

## Testing

```bash
cd backend
pytest tests/ -v
```

## License

For educational purposes.
