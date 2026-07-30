# Architecture rules

Keep these boundaries permanent:

1. **`website/`** — Next.js only (public school/college websites)
2. **`panel/`** — React (Vite) only (admin / teacher / student / parent panels)
3. **`backend/`** — FastAPI only (REST API, auth, tenancy, uploads)
4. **Database** — MySQL in production/docker (`DATABASE_URL=mysql+pymysql://...`)

Do not put website UI, panel UI, and API code in a single app folder again.

Frontends talk to backend via HTTP:

- Website → `GET /api/public/site/{slug}`
- Panel → `/api/auth/*`, `/api/admin/*`, etc.
