"""Seed demo tenants/users and enrich Greenfield with full website dummy content."""

from __future__ import annotations

import json

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.demo_media import ensure_greenfield_media
from app.models import (
    ContactInfo,
    GalleryImage,
    InstitutionType,
    Tenant,
    User,
    UserRole,
    WebsiteSettings,
)
from app.schema_upgrade import ensure_schema


SUBJECTS = {
    "primary": [
        "English",
        "Hindi",
        "Mathematics",
        "EVS",
        "Computer Basics",
        "Art & Craft",
        "Physical Education",
    ],
    "middle": [
        "English",
        "Hindi",
        "Mathematics",
        "Science",
        "Social Science",
        "Computer",
        "Sanskrit / Third Language",
    ],
    "secondary": [
        "English",
        "Hindi",
        "Mathematics",
        "Science (Physics, Chemistry, Biology)",
        "Social Science",
        "Information Technology",
    ],
    "senior": {
        "science": ["Physics", "Chemistry", "Mathematics / Biology", "English", "Computer Science / Physical Education"],
        "commerce": ["Accountancy", "Business Studies", "Economics", "English", "Mathematics / Informatics Practices"],
        "arts": ["History", "Political Science", "Geography / Sociology", "English", "Hindi / Psychology"],
    },
}

METHODOLOGY = """Greenfield follows a CBSE-aligned, student-centred approach:

1. Concept clarity first — lessons move from concrete examples to abstract thinking.
2. Continuous assessment — weekly checks, unit tests, and remedial support.
3. Activity-based learning — labs, projects, debates, and presentations.
4. Digital classrooms — smart boards and curated e-content in every section.
5. Mentorship — each student has a class teacher and subject mentors for Class 10 & 12.
6. Values & life skills — morning assembly, clubs, sports, and community service.

Board exams preparation for Class 10 and Class 12 includes timed practice papers, doubt clinics, and career counselling for Science, Commerce, and Arts streams."""


def _base_users_and_tenants(db) -> None:
    if db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first():
        return

    db.add(
        User(
            email="super@edunest.app",
            full_name="Platform Super Admin",
            hashed_password=hash_password("super123"),
            role=UserRole.SUPER_ADMIN,
            tenant_id=None,
        )
    )

    school = Tenant(
        name="Greenfield Public School",
        slug="greenfield",
        institution_type=InstitutionType.SCHOOL,
        tagline="CBSE excellence from Nursery to Class 12",
        about="Greenfield Public School is a CBSE-affiliated co-educational school offering Nursery to Class 12 with Science, Commerce, and Arts streams.",
        primary_color="#0b3d44",
        accent_color="#d4a017",
    )
    db.add(school)
    db.flush()

    for email, name, role, pwd in [
        ("admin@greenfield.edu", "School Admin", UserRole.ADMIN, "admin123"),
        ("teacher@greenfield.edu", "Anita Sharma", UserRole.TEACHER, "teacher123"),
        ("student@greenfield.edu", "Rahul Mehta", UserRole.STUDENT, "student123"),
        ("parent@greenfield.edu", "Priya Mehta", UserRole.PARENT, "parent123"),
    ]:
        db.add(
            User(
                tenant_id=school.id,
                email=email,
                full_name=name,
                hashed_password=hash_password(pwd),
                role=role,
            )
        )

    db.add(
        WebsiteSettings(
            tenant_id=school.id,
            hero_title="CBSE learning with character and confidence",
            hero_subtitle="Nursery to Class 12 · Science, Commerce & Arts · Toppers every year",
            hero_cta_text="Apply for admission",
            hero_cta_link="#admissions",
            about_heading="Welcome to Greenfield Public School",
            about_body=(
                "Greenfield Public School is a CBSE-affiliated co-educational day school in Pune.\n\n"
                "We offer a complete journey from Nursery to Class 12, with strong academics, "
                "caring teachers, and a campus culture of discipline, curiosity, and kindness."
            ),
            gallery_heading="Campus life at Greenfield",
            gallery_subtitle="Classrooms, labs, sports, library, and celebrations.",
            is_published=True,
        )
    )
    db.add(
        ContactInfo(
            tenant_id=school.id,
            address_line1="12 Lakeview Road",
            address_line2="Near City Park",
            city="Pune",
            state="Maharashtra",
            pincode="411001",
            country="India",
            phone_primary="+91 20 1234 5678",
            phone_secondary="+91 98765 43210",
            email="hello@greenfield.edu",
            email_admissions="admissions@greenfield.edu",
            working_hours="Mon–Sat · 8:00 AM – 2:30 PM",
            facebook_url="https://facebook.com",
            instagram_url="https://instagram.com",
        )
    )

    college = Tenant(
        name="Ridgeview College",
        slug="ridgeview",
        institution_type=InstitutionType.COLLEGE,
        tagline="Undergraduate excellence",
        primary_color="#1a365d",
        accent_color="#ed8936",
    )
    db.add(college)
    db.flush()
    db.add(
        User(
            tenant_id=college.id,
            email="admin@ridgeview.edu",
            full_name="College Admin",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
        )
    )
    db.add(
        WebsiteSettings(
            tenant_id=college.id,
            hero_title="Undergraduate excellence",
            hero_subtitle="Programs designed for careers that start with curiosity.",
            about_heading="About Ridgeview College",
            about_body="Supportive academics with clear career pathways.",
            is_published=True,
        )
    )
    db.add(ContactInfo(tenant_id=college.id, email="hello@ridgeview.edu", city="Mumbai", state="Maharashtra"))
    db.commit()
    print("Base tenants/users seeded.")


def enrich_greenfield(db) -> None:
    school = db.query(Tenant).filter(Tenant.slug == "greenfield").first()
    if not school:
        print("Greenfield tenant missing.")
        return

    media = ensure_greenfield_media()
    school.logo_path = media["logo"]
    school.tagline = "CBSE excellence from Nursery to Class 12"
    school.about = (
        "CBSE-affiliated co-educational school offering Nursery to Class 12 "
        "with Science, Commerce, and Arts streams."
    )

    website = db.query(WebsiteSettings).filter(WebsiteSettings.tenant_id == school.id).first()
    if not website:
        website = WebsiteSettings(tenant_id=school.id)
        db.add(website)
        db.flush()

    website.hero_title = "CBSE learning with character and confidence"
    website.hero_subtitle = "Nursery to Class 12 · Science, Commerce & Arts · Board toppers every year"
    website.hero_cta_text = "Apply for admission"
    website.hero_cta_link = "#admissions"
    website.hero_image_path = media["hero"]
    website.about_heading = "Welcome to Greenfield Public School"
    website.about_body = (
        "Greenfield Public School is a CBSE-affiliated co-educational day school in Pune.\n\n"
        "Students study from Nursery to Class 12. Senior secondary offers Science, Commerce, and Arts "
        "with focused board preparation, labs, sports, and values education."
    )
    website.about_image_path = media["about"]
    website.gallery_heading = "Campus life at Greenfield"
    website.gallery_subtitle = "Smart classrooms, labs, sports, library, and school events."
    website.board_name = "CBSE"
    website.classes_offered = "Nursery to Class 12"
    website.school_timings = "Monday to Saturday · 8:00 AM – 2:30 PM"
    website.assembly_time = "Morning assembly · 7:50 AM"
    website.streams_offered = "Class 11–12: Science, Commerce, Arts"
    website.subjects_json = json.dumps(SUBJECTS, ensure_ascii=False)
    website.methodology = METHODOLOGY
    website.toppers_json = json.dumps(media["toppers"], ensure_ascii=False)
    website.is_published = True

    contact = db.query(ContactInfo).filter(ContactInfo.tenant_id == school.id).first()
    if contact:
        contact.working_hours = "Mon–Sat · 8:00 AM – 2:30 PM"

    # Refresh gallery
    db.query(GalleryImage).filter(GalleryImage.tenant_id == school.id).delete()
    for item in media["gallery"]:
        db.add(
            GalleryImage(
                tenant_id=school.id,
                title=item["title"],
                caption=item["caption"],
                image_path=item["image_path"],
                sort_order=item["sort_order"],
                is_active=True,
            )
        )

    db.commit()
    print("Greenfield website enriched with academics, toppers, timings, and images.")


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_schema()
    db = SessionLocal()
    try:
        _base_users_and_tenants(db)
        enrich_greenfield(db)
        print("Seed complete.")
        print("Super Admin: super@edunest.app / super123")
        print("School Admin: admin@greenfield.edu / admin123 (tenant: greenfield)")
        print("Public site: /site/greenfield (Next.js) or legacy /site/greenfield on API host")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
