"""Download real school/human stock photos for Greenfield demo media."""

from __future__ import annotations

import urllib.request
from pathlib import Path

from app.config import get_settings

# Curated Unsplash images (school campus, classrooms, labs, sports, library, students/people)
IMAGE_URLS: dict[str, str] = {
    "hero.jpg": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1600&q=80",
    "about.jpg": "https://images.unsplash.com/photo-1577896851231-70ef18881754?auto=format&fit=crop&w=1400&q=80",
    "logo.jpg": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&h=800&q=80",
    "gallery_1.jpg": "https://images.unsplash.com/photo-1588072432836-e10032774350?auto=format&fit=crop&w=1400&q=80",
    "gallery_2.jpg": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1400&q=80",
    "gallery_3.jpg": "https://images.unsplash.com/photo-1517649763962-0c623066027e?auto=format&fit=crop&w=1400&q=80",
    "gallery_4.jpg": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1400&q=80",
    "gallery_5.jpg": "https://images.unsplash.com/photo-1523580494863-6f3031224c24?auto=format&fit=crop&w=1400&q=80",
    "gallery_6.jpg": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1400&q=80",
    "topper_1.jpg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=900&h=900&q=80",
    "topper_2.jpg": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=900&h=900&q=80",
    "topper_3.jpg": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&h=900&q=80",
    "topper_4.jpg": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=900&h=900&q=80",
}

GALLERY_META = [
    ("gallery_1.jpg", "Smart Classrooms", "Students learning in modern classrooms"),
    ("gallery_2.jpg", "Science Labs", "Hands-on experiments and discovery"),
    ("gallery_3.jpg", "Sports Ground", "Fitness, teamwork and outdoor games"),
    ("gallery_4.jpg", "Library", "Quiet reading and reference space"),
    ("gallery_5.jpg", "School Events", "Annual day, celebrations and assemblies"),
    ("gallery_6.jpg", "Computer Lab", "Digital skills and coding practice"),
]

TOPPERS_META = [
    ("topper_1.jpg", "Aarav Sharma", "Science", "Class 12", "97.2%"),
    ("topper_2.jpg", "Isha Patel", "Commerce", "Class 12", "96.4%"),
    ("topper_3.jpg", "Kabir Singh", "Arts", "Class 12", "95.8%"),
    ("topper_4.jpg", "Ananya Verma", "All subjects", "Class 10", "98.1%"),
]


def _download(url: str, dest: Path, force: bool = False) -> bool:
    if dest.exists() and dest.stat().st_size > 10_000 and not force:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "EduNestDemo/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < 1000:
            return False
        dest.write_bytes(data)
        print(f"Downloaded {dest.name} ({len(data)} bytes)")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"Failed {dest.name}: {exc}")
        return False


def ensure_greenfield_media(force: bool = False) -> dict:
    """Fetch real school/human photos into uploads and return public paths."""
    settings = get_settings()
    root = settings.upload_path / "greenfield"
    root.mkdir(parents=True, exist_ok=True)

    for name, url in IMAGE_URLS.items():
        ok = _download(url, root / name, force=force)
        if not ok and not (root / name).exists():
            raise RuntimeError(f"Could not download required demo image: {name}")

    gallery = []
    for i, (fname, title, caption) in enumerate(GALLERY_META):
        gallery.append(
            {
                "title": title,
                "caption": caption,
                "image_path": f"/uploads/greenfield/{fname}",
                "sort_order": i,
            }
        )

    toppers = []
    for fname, name, stream, klass, pct in TOPPERS_META:
        toppers.append(
            {
                "name": name,
                "class_name": klass,
                "stream": stream,
                "percentage": pct,
                "year": "2025",
                "photo_path": f"/uploads/greenfield/{fname}",
            }
        )

    return {
        "hero": "/uploads/greenfield/hero.jpg",
        "about": "/uploads/greenfield/about.jpg",
        "logo": "/uploads/greenfield/logo.jpg",
        "gallery": gallery,
        "toppers": toppers,
    }
