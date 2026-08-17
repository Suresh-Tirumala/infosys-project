#!/bin/bash
# Render build script
set -e

# Install Python dependencies
pip install -r backend/requirements.txt

# Install and build React frontend
cd frontend
npm install
npm run build
cd ..

# Copy React build into Django static directory for whitenoise to serve
mkdir -p backend/static/frontend
cp -r frontend/dist/* backend/static/frontend/

# Run Django migrations
cd backend
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
