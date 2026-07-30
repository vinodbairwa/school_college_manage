from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.middleware import LoginRedirectMiddleware
from app.routers import admin, auth, public, super_admin, web

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Legacy Jinja panels/site still work during migration; Next.js + React call /api/*
app.add_middleware(LoginRedirectMiddleware)

settings.upload_path.mkdir(parents=True, exist_ok=True)
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/uploads", StaticFiles(directory=str(settings.upload_path)), name="uploads")

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(super_admin.router)
app.include_router(admin.router)
app.include_router(web.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "db": "mysql" if settings.database_url.startswith("mysql") else "sqlite",
    }
