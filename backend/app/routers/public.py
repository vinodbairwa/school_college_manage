"""Public JSON APIs for the Next.js school website."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ContactInfo, GalleryImage, Tenant, WebsiteSettings
from app.schemas import (
    ContactInfoOut,
    GalleryImageOut,
    PublicSiteOut,
    TenantOut,
    WebsiteSettingsOut,
)

router = APIRouter(prefix="/api/public", tags=["public"])


@router.get("/tenants")
def list_public_tenants(db: Session = Depends(get_db)):
    tenants = (
        db.query(Tenant)
        .filter(Tenant.is_active.is_(True))
        .order_by(Tenant.name.asc())
        .all()
    )
    return [
        {
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "institution_type": t.institution_type.value,
            "tagline": t.tagline,
            "logo_path": t.logo_path,
            "primary_color": t.primary_color,
            "accent_color": t.accent_color,
        }
        for t in tenants
    ]


@router.get("/site/{slug}", response_model=PublicSiteOut)
def get_public_site(slug: str, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.slug == slug, Tenant.is_active.is_(True)).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="School not found")

    website = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    if website and not website.is_published:
        raise HTTPException(status_code=404, detail="Website not published")

    contact = db.query(ContactInfo).filter(ContactInfo.tenant_id == tenant.id).first()
    gallery = (
        db.query(GalleryImage)
        .filter(GalleryImage.tenant_id == tenant.id, GalleryImage.is_active.is_(True))
        .order_by(GalleryImage.sort_order, GalleryImage.id)
        .all()
    )

    return PublicSiteOut(
        tenant=TenantOut.model_validate(tenant),
        website=WebsiteSettingsOut.model_validate(website) if website else None,
        contact=ContactInfoOut.model_validate(contact) if contact else None,
        gallery=[GalleryImageOut.model_validate(g) for g in gallery],
    )
