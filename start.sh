#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"

echo "Seeding database (safe if already seeded)..."
python seed.py

echo "Starting EduNest on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
