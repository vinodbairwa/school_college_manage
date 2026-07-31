from pathlib import Path

from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth import ROLE_HOME, create_access_token, get_optional_user, verify_password
from app.config import get_settings
from app.database import get_db
from app.models import ContactInfo, GalleryImage, Tenant, User, UserRole, WebsiteSettings
from app.tenancy import get_tenant_or_none

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
settings = get_settings()

router = APIRouter(tags=["web"])


def _require_web_roles(*roles: UserRole):
    def checker(user: User | None = Depends(get_optional_user)) -> User:
        if not user:
            raise HTTPException(status_code=303, detail="login", headers={"Location": "/login"})
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return checker


def _website_context(db: Session, tenant: Tenant) -> dict:
    website = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == tenant.id).first()
    contact = db.query(ContactInfo).filter(ContactInfo.tenant_id == tenant.id).first()
    gallery = (
        db.query(GalleryImage)
        .filter(GalleryImage.tenant_id == tenant.id, GalleryImage.is_active.is_(True))
        .order_by(GalleryImage.sort_order, GalleryImage.id)
        .all()
    )
    return {"tenant": tenant, "website": website, "contact": contact, "gallery": gallery}


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    tenant: Tenant | None = Depends(get_tenant_or_none),
    user: User | None = Depends(get_optional_user),
):
    # Platform landing when no tenant resolved and explicit platform host
    if tenant is None:
        # Local demo: show first school site
        tenant = db.query(Tenant).filter(Tenant.is_active.is_(True)).order_by(Tenant.id.asc()).first()
        if tenant is None:
            return templates.TemplateResponse(
                "platform_home.html",
                {"request": request, "app_name": settings.app_name, "user": user},
            )

    ctx = _website_context(db, tenant)
    if ctx["website"] and not ctx["website"].is_published and (not user or user.tenant_id != tenant.id):
        raise HTTPException(status_code=404, detail="Website not published")

    return templates.TemplateResponse(
        "school/home.html",
        {"request": request, "user": user, **ctx},
    )


@router.get("/site/{slug}", response_class=HTMLResponse)
def site_by_slug(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    tenant = db.query(Tenant).filter(Tenant.slug == slug, Tenant.is_active.is_(True)).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="School not found")
    ctx = _website_context(db, tenant)
    return templates.TemplateResponse(
        "school/home.html",
        {"request": request, "user": user, **ctx},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)):
    if user:
        return RedirectResponse(ROLE_HOME.get(user.role, "/"), status_code=302)
    tenants = db.query(Tenant).filter(Tenant.is_active.is_(True)).order_by(Tenant.name).all()
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "tenants": tenants, "error": None, "app_name": settings.app_name},
    )


@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    tenant_slug: str = Form(""),
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.email == email.lower())
    if tenant_slug:
        tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
        user = query.filter(User.tenant_id == tenant.id).first() if tenant else None
    else:
        user = query.filter(User.role == UserRole.SUPER_ADMIN).first() or query.first()

    tenants = db.query(Tenant).filter(Tenant.is_active.is_(True)).order_by(Tenant.name).all()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "tenants": tenants,
                "error": "Invalid email or password",
                "app_name": settings.app_name,
            },
            status_code=401,
        )

    token = create_access_token(
        {"sub": str(user.id), "role": user.role.value, "tenant_id": user.tenant_id},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    resp = RedirectResponse(ROLE_HOME[user.role], status_code=302)
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.access_token_expire_minutes * 60,
    )
    return resp


@router.get("/logout")
def logout():
    resp = RedirectResponse("/login", status_code=302)
    resp.delete_cookie("access_token")
    return resp


@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(_require_web_roles(UserRole.ADMIN)),
):
    tenant = db.get(Tenant, user.tenant_id)
    ctx = _website_context(db, tenant)
    return templates.TemplateResponse(
        "panels/admin.html",
        {"request": request, "user": user, "active": "dashboard", **ctx},
    )


@router.get("/admin/website", response_class=HTMLResponse)
def admin_website(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(_require_web_roles(UserRole.ADMIN)),
):
    tenant = db.get(Tenant, user.tenant_id)
    ctx = _website_context(db, tenant)
    return templates.TemplateResponse(
        "panels/admin_website.html",
        {"request": request, "user": user, "active": "website", **ctx},
    )


@router.get("/admin/gallery", response_class=HTMLResponse)
def admin_gallery(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(_require_web_roles(UserRole.ADMIN)),
):
    tenant = db.get(Tenant, user.tenant_id)
    ctx = _website_context(db, tenant)
    return templates.TemplateResponse(
        "panels/admin_gallery.html",
        {"request": request, "user": user, "active": "gallery", **ctx},
    )


@router.get("/admin/contact", response_class=HTMLResponse)
def admin_contact(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(_require_web_roles(UserRole.ADMIN)),
):
    tenant = db.get(Tenant, user.tenant_id)
    ctx = _website_context(db, tenant)
    return templates.TemplateResponse(
        "panels/admin_contact.html",
        {"request": request, "user": user, "active": "contact", **ctx},
    )


@router.get("/super-admin", response_class=HTMLResponse)
def super_admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(_require_web_roles(UserRole.SUPER_ADMIN)),
):
    tenants = db.query(Tenant).order_by(Tenant.created_at.desc()).all()
    return templates.TemplateResponse(
        "panels/super_admin.html",
        {"request": request, "user": user, "tenants": tenants, "app_name": settings.app_name},
    )


@router.get("/teacher", response_class=HTMLResponse)
def teacher_panel(request: Request, user: User = Depends(_require_web_roles(UserRole.TEACHER))):
    return templates.TemplateResponse(
        "panels/role_stub.html",
        {
            "request": request,
            "user": user,
            "panel_title": "Teacher Panel",
            "panel_note": "Attendance, classes, and assignments will appear here next.",
        },
    )


@router.get("/student", response_class=HTMLResponse)
def student_panel(request: Request, user: User = Depends(_require_web_roles(UserRole.STUDENT))):
    return templates.TemplateResponse(
        "panels/role_stub.html",
        {
            "request": request,
            "user": user,
            "panel_title": "Student Panel",
            "panel_note": "Timetable, results, and fees will appear here next.",
        },
    )


@router.get("/parent", response_class=HTMLResponse)
def parent_panel(request: Request, user: User = Depends(_require_web_roles(UserRole.PARENT))):
    return templates.TemplateResponse(
        "panels/role_stub.html",
        {
            "request": request,
            "user": user,
            "panel_title": "Parent Panel",
            "panel_note": "Child progress, notices, and fee updates will appear here next.",
        },
    )
