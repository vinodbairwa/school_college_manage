from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import InstitutionType, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    redirect_to: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_slug: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: UserRole
    tenant_id: Optional[int] = None
    is_active: bool


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    institution_type: InstitutionType = InstitutionType.SCHOOL
    custom_domain: Optional[str] = None
    tagline: Optional[str] = None
    admin_email: EmailStr
    admin_password: str = Field(min_length=6)
    admin_name: str = Field(min_length=2)


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    about: Optional[str] = None
    custom_domain: Optional[str] = None
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    is_active: Optional[bool] = None
    institution_type: Optional[InstitutionType] = None


class TenantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    institution_type: InstitutionType
    custom_domain: Optional[str] = None
    is_active: bool
    tagline: Optional[str] = None
    about: Optional[str] = None
    logo_path: Optional[str] = None
    primary_color: str
    accent_color: str
    created_at: datetime


class WebsiteSettingsUpdate(BaseModel):
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    hero_cta_text: Optional[str] = None
    hero_cta_link: Optional[str] = None
    about_heading: Optional[str] = None
    about_body: Optional[str] = None
    gallery_heading: Optional[str] = None
    gallery_subtitle: Optional[str] = None
    is_published: Optional[bool] = None


class WebsiteSettingsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    hero_image_path: Optional[str] = None
    hero_cta_text: str
    hero_cta_link: str
    about_heading: Optional[str] = None
    about_body: Optional[str] = None
    about_image_path: Optional[str] = None
    gallery_heading: str
    gallery_subtitle: Optional[str] = None
    is_published: bool


class GalleryImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str] = None
    caption: Optional[str] = None
    image_path: str
    sort_order: int
    is_active: bool


class ContactInfoUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    phone_primary: Optional[str] = None
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    email_admissions: Optional[str] = None
    map_embed_url: Optional[str] = None
    working_hours: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None


class ContactInfoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: str
    phone_primary: Optional[str] = None
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    email_admissions: Optional[str] = None
    map_embed_url: Optional[str] = None
    working_hours: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None


class PublicSiteOut(BaseModel):
    tenant: TenantOut
    website: Optional[WebsiteSettingsOut] = None
    contact: Optional[ContactInfoOut] = None
    gallery: list[GalleryImageOut] = []


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=6)
    role: UserRole
    phone: Optional[str] = None
