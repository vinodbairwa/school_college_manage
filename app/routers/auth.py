from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import ROLE_HOME, create_access_token, get_current_user, verify_password
from app.config import get_settings
from app.database import get_db
from app.models import Tenant, User, UserRole
from app.schemas import LoginRequest, Token, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return _authenticate(db, response, form_data.username, form_data.password, tenant_slug=None)


@router.post("/login-json", response_model=Token)
def login_json(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return _authenticate(db, response, payload.email, payload.password, payload.tenant_slug)


@router.post("/login-form", response_model=Token)
def login_form(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    tenant_slug: str | None = Form(None),
    db: Session = Depends(get_db),
):
    return _authenticate(db, response, email, password, tenant_slug)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True}


def _authenticate(
    db: Session,
    response: Response,
    email: str,
    password: str,
    tenant_slug: str | None,
) -> Token:
    query = db.query(User).filter(User.email == email.lower())

    if tenant_slug:
        tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
        if not tenant:
            raise HTTPException(status_code=400, detail="Unknown tenant")
        user = query.filter(User.tenant_id == tenant.id).first()
    else:
        user = query.filter(User.role == UserRole.SUPER_ADMIN).first() or query.first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _issue_token(response, user)


def _issue_token(response: Response, user: User) -> Token:
    token = create_access_token(
        {"sub": str(user.id), "role": user.role.value, "tenant_id": user.tenant_id},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return Token(access_token=token, role=user.role, redirect_to=ROLE_HOME[user.role])


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
