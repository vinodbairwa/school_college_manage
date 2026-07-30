"""Generate simple demo images for Greenfield (no external downloads)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings


def _font(size: int):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _gradient(size: tuple[int, int], c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / max(h - 1, 1)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def _label(img: Image.Image, title: str, subtitle: str = "") -> Image.Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle([(0, h - 120), (w, h)], fill=(8, 28, 32, 180) if img.mode == "RGBA" else (8, 28, 32))
    draw.text((36, h - 95), title, fill=(255, 255, 255), font=_font(36))
    if subtitle:
        draw.text((36, h - 50), subtitle, fill=(230, 220, 180), font=_font(20))
    return img


def make_demo_image(rel_path: str, title: str, subtitle: str, colors: tuple[tuple[int, int, int], tuple[int, int, int]], size=(1600, 900)) -> str:
    settings = get_settings()
    out = settings.upload_path / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    img = _gradient(size, colors[0], colors[1])
    # subtle grid
    draw = ImageDraw.Draw(img)
    for x in range(0, size[0], 48):
        draw.line([(x, 0), (x, size[1])], fill=(255, 255, 255, 20) if False else (255, 255, 255))
        # lighten by blending manually - skip for simplicity
    _label(img, title, subtitle)
    img.save(out, quality=88)
    return f"/uploads/{rel_path.replace(chr(92), '/')}"


def ensure_greenfield_media() -> dict[str, str | list[dict]]:
    """Create demo media files and return public paths."""
    hero = make_demo_image(
        "greenfield/hero.jpg",
        "Greenfield Public School",
        "CBSE · Nursery to Class 12",
        ((11, 61, 68), (19, 96, 102)),
    )
    about = make_demo_image(
        "greenfield/about.jpg",
        "Campus & Classrooms",
        "Safe spaces for every learner",
        ((20, 70, 78), (45, 110, 100)),
        size=(1200, 900),
    )
    logo = make_demo_image(
        "greenfield/logo.jpg",
        "GPS",
        "Greenfield",
        ((212, 160, 23), (11, 61, 68)),
        size=(400, 400),
    )
    gallery = []
    specs = [
        ("gallery_1.jpg", "Smart Classrooms", "Digital learning every day"),
        ("gallery_2.jpg", "Science Labs", "Hands-on experiments"),
        ("gallery_3.jpg", "Sports Ground", "Fitness and teamwork"),
        ("gallery_4.jpg", "Library", "Reading corner & reference"),
        ("gallery_5.jpg", "Annual Day", "Culture and confidence"),
        ("gallery_6.jpg", "Computer Lab", "Coding & digital skills"),
    ]
    colors = [
        ((40, 90, 95), (70, 130, 120)),
        ((55, 80, 110), (30, 60, 90)),
        ((90, 110, 60), (50, 80, 50)),
        ((100, 80, 50), (60, 50, 35)),
        ((90, 50, 70), (50, 30, 50)),
        ((40, 70, 100), (20, 40, 70)),
    ]
    for i, ((fname, title, caption), cols) in enumerate(zip(specs, colors)):
        path = make_demo_image(f"greenfield/{fname}", title, caption, cols, size=(1200, 800))
        gallery.append({"title": title, "caption": caption, "image_path": path, "sort_order": i})

    toppers = []
    for i, (name, stream, klass, pct) in enumerate(
        [
            ("Aarav Sharma", "Science", "Class 12", "97.2%"),
            ("Isha Patel", "Commerce", "Class 12", "96.4%"),
            ("Kabir Singh", "Arts", "Class 12", "95.8%"),
            ("Ananya Verma", "All subjects", "Class 10", "98.1%"),
        ]
    ):
        path = make_demo_image(
            f"greenfield/topper_{i+1}.jpg",
            name,
            f"{klass} · {stream} · {pct}",
            ((30, 70, 80), (180, 140, 40)),
            size=(800, 800),
        )
        toppers.append(
            {
                "name": name,
                "class_name": klass,
                "stream": stream,
                "percentage": pct,
                "year": "2025",
                "photo_path": path,
            }
        )

    return {"hero": hero, "about": about, "logo": logo, "gallery": gallery, "toppers": toppers}
