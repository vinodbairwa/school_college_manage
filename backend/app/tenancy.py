from typing import Optional

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Tenant

settings = get_settings()


def extract_host(request: Request) -> str:
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
    return host.split(":")[0].lower().strip()


def resolve_tenant_slug(request: Request) -> Optional[str]:
    """Resolve tenant from custom domain, subdomain, query, or path hint."""
    host = extract_host(request)
    base = settings.base_domain.lower()

    # Explicit query override for local/dev: ?tenant=demo
    query_slug = request.query_params.get("tenant")
    if query_slug:
        return query_slug.lower()

    # Header override (useful behind reverse proxy)
    header_slug = request.headers.get("x-tenant-slug")
    if header_slug:
        return header_slug.lower()

    if not host or host in {"localhost", "127.0.0.1", base}:
        return None

    # Custom domain: exact host match handled in DB lookup
    if not host.endswith(base) and host not in {base, f"www.{base}"}:
        return f"domain:{host}"

    # Subdomain: demo.localhost or demo.edunest.com
    if host.endswith(f".{base}"):
        sub = host[: -(len(base) + 1)]
        if sub and sub != "www":
            return sub.split(".")[0]

    return None


def get_tenant_or_none(request: Request, db: Session = Depends(get_db)) -> Optional[Tenant]:
    slug = resolve_tenant_slug(request)
    if not slug:
        return None

    if slug.startswith("domain:"):
        domain = slug.replace("domain:", "", 1)
        return db.query(Tenant).filter(Tenant.custom_domain == domain, Tenant.is_active.is_(True)).first()

    return db.query(Tenant).filter(Tenant.slug == slug, Tenant.is_active.is_(True)).first()


def get_tenant_required(request: Request, db: Session = Depends(get_db)) -> Tenant:
    tenant = get_tenant_or_none(request, db)
    if not tenant:
        # Fallback: first active school for local demo when no slug
        slug = resolve_tenant_slug(request)
        if not slug:
            tenant = (
                db.query(Tenant)
                .filter(Tenant.is_active.is_(True))
                .order_by(Tenant.id.asc())
                .first()
            )
        if not tenant:
            raise HTTPException(status_code=404, detail="School / tenant not found")
    return tenant
