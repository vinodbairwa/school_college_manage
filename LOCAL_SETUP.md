# EduNest local setup (Windows / Mac / Linux)

## Fix: "Backend API is not reachable"

This means **FastAPI is not running on port 8000**.
Running only `website` is not enough.

### Correct way (all 3 together)

From the **project root** (`school_college_manage`):

```bash
npm install
npm start
```

Wait until you see backend + website + panel started, then open:

- Website: http://127.0.0.1:3000/site/greenfield
- Panel: http://127.0.0.1:5173/login
- Backend health: http://127.0.0.1:8000/health

### If backend still fails

1. Install **Python 3.12+** and ensure `python --version` works in terminal
2. From root:

```bash
python -m venv .venv
```

Windows:
```bat
.venv\Scripts\python -m pip install -r backend\requirements.txt
cd backend
..\.venv\Scripts\python seed.py
..\.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mac/Linux:
```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. In another terminal start website:
```bash
cd website
npm install
npm run dev
```

4. Open http://127.0.0.1:8000/health — must show `{"status":"ok",...}`

### Common mistakes

- Started only `cd website && npm run dev` (backend missing)
- Used old `bash` scripts on Windows without Git Bash (use `npm start` now)
- Python not installed / not on PATH
- Port 8000 already used by another app
