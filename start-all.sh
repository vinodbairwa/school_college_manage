#!/usr/bin/env bash
# Start EduNest: backend (FastAPI) + website (Next.js) + panel (React) together.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "==> EduNest all-in-one starter"
echo "    backend  : http://127.0.0.1:8000"
echo "    website  : http://127.0.0.1:3000"
echo "    panel    : http://127.0.0.1:5173"
echo

# Python venv
if [[ ! -d .venv ]]; then
  echo "==> Creating Python venv..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing backend deps..."
pip install -q -r backend/requirements.txt

if [[ ! -f backend/.env ]]; then
  cp backend/.env.example backend/.env
fi

echo "==> Seeding database (safe if already seeded)..."
(cd backend && python seed.py)

# Node deps
if [[ ! -d node_modules ]]; then
  echo "==> Installing root (concurrently)..."
  npm install
fi
if [[ ! -d website/node_modules ]]; then
  echo "==> Installing website deps..."
  npm --prefix website install
fi
if [[ ! -d panel/node_modules ]]; then
  echo "==> Installing panel deps..."
  npm --prefix panel install
fi

if [[ ! -f website/.env.local ]]; then
  cp website/.env.local.example website/.env.local 2>/dev/null || true
fi
if [[ ! -f panel/.env ]]; then
  cp panel/.env.example panel/.env 2>/dev/null || true
fi

# Free ports if previous runs left processes
for port in 8000 3000 5173; do
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "${port}/tcp" >/dev/null 2>&1 || true
  fi
done
sleep 1

echo "==> Starting all three services..."
exec npm run dev
