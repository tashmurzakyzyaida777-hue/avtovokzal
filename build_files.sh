#!/bin/bash
echo "==> Building project on Vercel..."

echo "==> Installing Python dependencies..."
python3 -m pip install -r requirements.txt

echo "==> Collecting static files..."
python3 manage.py collectstatic --noinput

echo "==> Running database migrations..."
# Note: Migrations will run if DATABASE_URL environment variable is set.
python3 manage.py migrate --noinput

echo "==> Build completed successfully!"
