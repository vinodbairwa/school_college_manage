# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

EduNest is a single-service Python monolith (FastAPI + Jinja2). There is no separate frontend, Docker Compose, or test suite. See `README.md` for full quick-start and demo accounts.

### Required services

| Service | Port | Notes |
|---------|------|-------|
| FastAPI (Uvicorn) | 8000 | Only process that must run for local dev |
| SQLite | — | Embedded file DB (`school_saas.db`); no separate server |

### One-time setup (first run on a fresh VM)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # if .env does not exist
python seed.py         # creates demo tenants/users; safe to re-run
```

If `python3 -m venv` fails with "ensurepip is not available", install the system package first: `sudo apt-get install -y python3.12-venv`.

### Running the dev server

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Lint / test

This repo has no configured linter or automated test suite. Use `python -m compileall -q app seed.py` as a basic syntax check. Smoke-test via `curl http://127.0.0.1:8000/health` and the API docs at `/docs`.

### Key URLs

- Public demo site: http://127.0.0.1:8000/site/greenfield
- Login: http://127.0.0.1:8000/login
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### Demo credentials

| Role | Email | Password | Tenant |
|------|-------|----------|--------|
| Super Admin | `super@edunest.app` | `super123` | Platform Super Admin |
| School Admin | `admin@greenfield.edu` | `admin123` | Greenfield Public School |

### Gotchas

- `seed.py` may log a harmless bcrypt version warning from passlib; seeding still succeeds.
- The `uploads/` directory and `school_saas.db` are created at runtime and are gitignored.
- Re-seeding is idempotent for demo data; deleting `school_saas.db` and re-running `seed.py` resets the DB.
