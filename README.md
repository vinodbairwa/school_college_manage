# EduNest — School / College / University SaaS (FastAPI)

Multi-tenant education SaaS with role panels and a **dynamic public school website** managed from the admin panel (images + contact).

## Features (current)

- **Multi-tenant SaaS**: each school/college/university is a tenant (`slug` + optional **custom domain**)
- **Roles**: Super Admin, Admin, Teacher, Student, Parent
- **Public school website**: hero, about, gallery, contact — content & images from Admin panel
- **Tenant resolution**: custom domain, subdomain (`{slug}.localhost`), or `/site/{slug}`
- **JWT cookie auth** for web panels + JSON/API login

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- Public demo school: http://127.0.0.1:8000/site/greenfield
- Login: http://127.0.0.1:8000/login
- API docs: http://127.0.0.1:8000/docs

## Demo accounts

| Role | Email | Password | Tenant select |
|------|-------|----------|---------------|
| Super Admin | `super@edunest.app` | `super123` | Platform Super Admin |
| School Admin | `admin@greenfield.edu` | `admin123` | Greenfield Public School |
| Teacher | `teacher@greenfield.edu` | `teacher123` | Greenfield… |
| Student | `student@greenfield.edu` | `student123` | Greenfield… |
| Parent | `parent@greenfield.edu` | `parent123` | Greenfield… |

## Admin: dynamic website

After logging in as school admin:

1. **Website & Images** — hero/about text, hero image, about image, logo  
2. **Gallery** — upload campus photos  
3. **Contact** — address, phones, emails, map embed, social links  

Changes show immediately on `/site/greenfield`.

## Custom domain (SaaS)

1. Super Admin creates a tenant (or Admin sets domain) with e.g. `www.myschool.com`
2. Point the client DNS (A/CNAME) to your server
3. Reverse proxy (nginx/Caddy) forwards Host header to this app  
4. App resolves tenant by `Tenant.custom_domain`

Local/dev overrides:

- `/site/{slug}`
- `?tenant=greenfield`
- Header `X-Tenant-Slug: greenfield`

## Project layout

```
app/
  main.py           # FastAPI app
  models.py         # Tenant, User, Website, Gallery, Contact
  auth.py           # JWT + roles
  tenancy.py        # Domain / subdomain resolution
  routers/          # auth, admin, super-admin, web UI
  templates/        # School site + panels (Jinja2)
  static/css/       # Site styles
seed.py
```

## Next (planned)

- Full teacher / student / parent modules (attendance, results, fees)
- College & university website templates
- Billing / subscription per tenant
- Alembic migrations + PostgreSQL for production
