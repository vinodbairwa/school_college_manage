"""Seed demo tenants and users."""
from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import (
    ContactInfo,
    GalleryImage,
    InstitutionType,
    Tenant,
    User,
    UserRole,
    WebsiteSettings,
)


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first():
            print("Already seeded.")
            return

        super_admin = User(
            email="super@edunest.app",
            full_name="Platform Super Admin",
            hashed_password=hash_password("super123"),
            role=UserRole.SUPER_ADMIN,
            tenant_id=None,
        )
        db.add(super_admin)

        school = Tenant(
            name="Greenfield Public School",
            slug="greenfield",
            institution_type=InstitutionType.SCHOOL,
            custom_domain=None,
            tagline="Where every learner finds their voice",
            about="Greenfield is a K-12 school focused on curiosity, craft, and community.",
            primary_color="#0b3d44",
            accent_color="#d4a017",
        )
        db.add(school)
        db.flush()

        db.add(
            User(
                tenant_id=school.id,
                email="admin@greenfield.edu",
                full_name="School Admin",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
            )
        )
        db.add(
            User(
                tenant_id=school.id,
                email="teacher@greenfield.edu",
                full_name="Anita Sharma",
                hashed_password=hash_password("teacher123"),
                role=UserRole.TEACHER,
            )
        )
        db.add(
            User(
                tenant_id=school.id,
                email="student@greenfield.edu",
                full_name="Rahul Mehta",
                hashed_password=hash_password("student123"),
                role=UserRole.STUDENT,
            )
        )
        db.add(
            User(
                tenant_id=school.id,
                email="parent@greenfield.edu",
                full_name="Priya Mehta",
                hashed_password=hash_password("parent123"),
                role=UserRole.PARENT,
            )
        )

        db.add(
            WebsiteSettings(
                tenant_id=school.id,
                hero_title="Learning that feels alive",
                hero_subtitle="Strong academics, warm guidance, and a campus where every student belongs.",
                hero_cta_text="Apply for admission",
                hero_cta_link="#admissions",
                about_heading="A school rooted in care and excellence",
                about_body=(
                    "Greenfield Public School is committed to academic excellence, character formation, "
                    "and a safe campus for every learner.\n\n"
                    "We blend rigorous classroom teaching with arts, sports, and life skills — so students "
                    "grow into confident, curious, and responsible young people. Parents and teachers "
                    "partner closely so every child is known, challenged, and celebrated."
                ),
                gallery_heading="Life on campus",
                gallery_subtitle="Classrooms, sports, celebrations, and everyday moments of learning.",
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
                working_hours="Mon–Sat · 8:30 AM – 3:30 PM",
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
                hero_subtitle="Programs designed for careers that start with curiosity, discipline, and real-world skills.",
                hero_cta_text="Talk to admissions",
                hero_cta_link="#admissions",
                about_heading="About Ridgeview College",
                about_body=(
                    "Ridgeview College offers a supportive academic environment with experienced faculty, "
                    "clear career pathways, and an active campus life.\n\n"
                    "Students receive guidance for academics, personal growth, and future opportunities — "
                    "in a community that values integrity and achievement."
                ),
                gallery_heading="Campus moments",
                gallery_subtitle="Academics, clubs, events, and student life at Ridgeview.",
                is_published=True,
            )
        )
        db.add(ContactInfo(tenant_id=college.id, email="hello@ridgeview.edu", city="Mumbai", state="Maharashtra"))

        db.commit()
        print("Seed complete.")
        print("Super Admin: super@edunest.app / super123")
        print("School Admin: admin@greenfield.edu / admin123 (tenant: greenfield)")
        print("Teacher/Student/Parent: teacher@ / student@ / parent@ greenfield.edu")
        print("Public site: /site/greenfield")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
