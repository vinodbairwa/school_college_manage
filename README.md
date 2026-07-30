# EduNest — School / College SaaS (monorepo)

Architecture (keep code separated):

```
backend/   → FastAPI + MySQL (API, auth, tenancy, uploads)
website/   → Next.js (public dynamic school websites)
panel/     → React (Vite) (admin / teacher / student / parent panels)
```

Do **not** put website + panel + API all in one app folder.

## Folders

| Folder | Stack | Purpose |
|--------|--------|---------|
| `backend/` | FastAPI, SQLAlchemy, MySQL | REST API, JWT auth, multi-tenant data |
| `website/` | Next.js 15 | Public school/college websites |
| `panel/` | React + Vite | Logged-in role panels |

## Quick start (testing branch)

### 1) Backend (API)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://127.0.0.1:8000/docs  
Public site JSON: http://127.0.0.1:8000/api/public/site/greenfield

### 2) MySQL (optional, recommended)

```bash
docker compose up -d mysql
```

Then in `backend/.env`:

```env
DATABASE_URL=mysql+pymysql://edunest:edunest@127.0.0.1:3306/edunest
```

Re-run `python seed.py`.

### 3) Website (Next.js)

```bash
cd website
cp .env.local.example .env.local
npm install
npm run dev
```

Open: http://127.0.0.1:3000/site/greenfield

### 4) Panel (React)

```bash
cd panel
cp .env.example .env
npm install
npm run dev
```

Open: http://127.0.0.1:5173/login

## Demo accounts

| Role | Email | Password | Tenant |
|------|-------|----------|--------|
| Super Admin | `super@edunest.app` | `super123` | (blank) |
| School Admin | `admin@greenfield.edu` | `admin123` | greenfield |
| Teacher | `teacher@greenfield.edu` | `teacher123` | greenfield |

## Notes

- Legacy Jinja templates still exist under `backend/app/templates` during migration.
- New work: public UI → `website/`, panels → `panel/`, APIs → `backend/`.
- Branch policy: develop on `cursor/testing-de89` — do not merge to `main` until approved.
