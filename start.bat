@echo off
title HealthBot AI - Starting Services
echo.
echo ========================================
echo   HealthBot AI - Starting Services...
echo ========================================
echo.

echo [1/2] Starting Backend (Django) on port 8000...
start "HealthBot Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py runserver"

echo [2/2] Starting Frontend (Vite) on port 5173...
start "HealthBot Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Both services are starting up!
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Close the opened windows to stop each service.
pause
