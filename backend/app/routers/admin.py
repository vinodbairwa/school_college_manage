from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import require_roles
from app.database import get_db
from app.models import ContactInfo, GalleryImage, Tenant, User, UserRole, WebsiteSettings
from app.schemas import (
    ContactInfoOut,
    ContactInfoUpdate,
    GalleryImageOut,
    TenantOut,
    TenantUpdate,
    WebsiteSettingsOut,
    WebsiteSettingsUpdate,
)
from app.uploads import save_upload

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _tenant_for_admin(user: User, db: Session) -> Tenant:
    if user.role == UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=400, detail="Use tenant-scoped admin account")
    if not user.tenant_id:
        raise HTTPException(status_code=400, detail="No tenant linked")
    tenant = db.get(Tenant, user.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.get("/tenant", response_model=TenantOut)
def get_my_tenant(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return _tenant_for_admin(user, db)


@router.patch("/tenant", response_model=TenantOut)
def update_my_tenant(
    payload: TenantUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    data = payload.model_dump(exclude_unset=True)
    # Admins cannot deactivate tenant or change institution type freely via this endpoint — allow branding fields
    allowed = {"name", "tagline", "about", "custom_domain", "primary_color", "accent_color"}
    for key, value in data.items():
        if key in allowed:
            setattr(tenant, key, value)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.post("/tenant/logo", response_model=TenantOut)
async def upload_logo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    tenant.logo_path = await save_upload(file, tenant.slug, "logo")
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("/website", response_model=WebsiteSettingsOut)
def get_website(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    settings = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    if not settings:
        settings = WebsiteSettings(tenant_id=tenant.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.patch("/website", response_model=WebsiteSettingsOut)
def update_website(
    payload: WebsiteSettingsUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    settings = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    if not settings:
        settings = WebsiteSettings(tenant_id=tenant.id)
        db.add(settings)
        db.flush()
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings


@router.post("/website/hero-image", response_model=WebsiteSettingsOut)
async def upload_hero_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    settings = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    if not settings:
        settings = WebsiteSettings(tenant_id=tenant.id)
        db.add(settings)
        db.flush()
    settings.hero_image_path = await save_upload(file, tenant.slug, "hero")
    db.commit()
    db.refresh(settings)
    return settings


@router.post("/website/about-image", response_model=WebsiteSettingsOut)
async def upload_about_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    settings = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    if not settings:
        settings = WebsiteSettings(tenant_id=tenant.id)
        db.add(settings)
        db.flush()
    settings.about_image_path = await save_upload(file, tenant.slug, "about")
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/gallery", response_model=list[GalleryImageOut])
def list_gallery(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    return (
        db.query(GalleryImage)
        .filter(GalleryImage.tenant_id == tenant.id)
        .order_by(GalleryImage.sort_order, GalleryImage.id)
        .all()
    )


@router.post("/gallery", response_model=GalleryImageOut)
async def add_gallery_image(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    caption: str | None = Form(None),
    sort_order: int = Form(0),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    path = await save_upload(file, tenant.slug, "gallery")
    image = GalleryImage(
        tenant_id=tenant.id,
        title=title,
        caption=caption,
        image_path=path,
        sort_order=sort_order,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.delete("/gallery/{image_id}")
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    image = db.query(GalleryImage).filter(GalleryImage.id == image_id, GalleryImage.tenant_id == tenant.id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"ok": True}


@router.get("/contact", response_model=ContactInfoOut)
def get_contact(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    contact = db.query(ContactInfo).filter(ContactInfo.tenant_id == tenant.id).first()
    if not contact:
        contact = ContactInfo(tenant_id=tenant.id)
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact


@router.patch("/contact", response_model=ContactInfoOut)
def update_contact(
    payload: ContactInfoUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.ADMIN)),
):
    tenant = _tenant_for_admin(user, db)
    contact = db.query(ContactInfo).filter(ContactInfo.tenant_id == tenant.id).first()
    if not contact:
        contact = ContactInfo(tenant_id=tenant.id)
        db.add(contact)
        db.flush()
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact
