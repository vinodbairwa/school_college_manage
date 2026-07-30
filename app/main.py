from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.middleware import LoginRedirectMiddleware
from app.routers import admin, auth, super_admin, web

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")
# Trust X-Forwarded-* from Render / Cloudflare / reverse proxies
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.add_middleware(LoginRedirectMiddleware)

# Ensure upload + static dirs exist
settings.upload_path.mkdir(parents=True, exist_ok=True)
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/uploads", StaticFiles(directory=str(settings.upload_path)), name="uploads")

app.include_router(auth.router)
app.include_router(super_admin.router)
app.include_router(admin.router)
app.include_router(web.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
