from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import hash_password, require_roles
from app.database import get_db
from app.models import ContactInfo, Tenant, User, UserRole, WebsiteSettings
from app.schemas import TenantCreate, TenantOut, TenantUpdate

router = APIRouter(prefix="/api/super-admin", tags=["super-admin"])


@router.get("/tenants", response_model=list[TenantOut])
def list_tenants(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
):
    return db.query(Tenant).order_by(Tenant.created_at.desc()).all()


@router.post("/tenants", response_model=TenantOut)
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
):
    if db.query(Tenant).filter(Tenant.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")
    if payload.custom_domain and db.query(Tenant).filter(Tenant.custom_domain == payload.custom_domain).first():
        raise HTTPException(status_code=400, detail="Custom domain already in use")

    tenant = Tenant(
        name=payload.name,
        slug=payload.slug,
        institution_type=payload.institution_type,
        custom_domain=payload.custom_domain,
        tagline=payload.tagline,
    )
    db.add(tenant)
    db.flush()

    admin = User(
        tenant_id=tenant.id,
        email=payload.admin_email.lower(),
        full_name=payload.admin_name,
        hashed_password=hash_password(payload.admin_password),
        role=UserRole.ADMIN,
    )
    db.add(admin)
    db.add(
        WebsiteSettings(
            tenant_id=tenant.id,
            hero_title=payload.name,
            hero_subtitle=payload.tagline or "Welcome to our campus",
            about_heading=f"About {payload.name}",
            about_body="Update this section from the admin panel.",
        )
    )
    db.add(ContactInfo(tenant_id=tenant.id, email=payload.admin_email.lower()))
    db.commit()
    db.refresh(tenant)
    return tenant


@router.patch("/tenants/{tenant_id}", response_model=TenantOut)
def update_tenant(
    tenant_id: int,
    payload: TenantUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
):
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tenant, key, value)
    db.commit()
    db.refresh(tenant)
    return tenant
