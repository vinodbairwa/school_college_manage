"""Lightweight schema upgrades for SQLite/MySQL without Alembic."""

from sqlalchemy import inspect, text

from app.database import engine

WEBSITE_COLUMNS = {
    "board_name": "VARCHAR(100)",
    "classes_offered": "VARCHAR(200)",
    "school_timings": "VARCHAR(300)",
    "assembly_time": "VARCHAR(100)",
    "streams_offered": "VARCHAR(300)",
    "subjects_json": "TEXT",
    "methodology": "TEXT",
    "toppers_json": "TEXT",
}


def ensure_schema() -> None:
    inspector = inspect(engine)
    if "website_settings" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("website_settings")}
    dialect = engine.dialect.name
    with engine.begin() as conn:
        for name, col_type in WEBSITE_COLUMNS.items():
            if name in existing:
                continue
            if dialect == "sqlite":
                conn.execute(text(f"ALTER TABLE website_settings ADD COLUMN {name} {col_type}"))
            else:
                conn.execute(text(f"ALTER TABLE website_settings ADD COLUMN {name} {col_type} NULL"))
            print(f"Added column website_settings.{name}")
