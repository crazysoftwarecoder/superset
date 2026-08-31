"""Export utilities for scheduled report delivery."""

import gzip
import os
import secrets
import shutil
import sqlite3
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from markupsafe import escape

EXPORTS_DB = "exports.db"
EXPORTS_DIR = Path("/var/exports")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
DOWNLOAD_TOKEN_BYTES = 32
ALLOWED_LINK_SCHEMES = {"http", "https"}


def get_export_by_name(name: str) -> Optional[tuple[int, str, str]]:
    """Look up an export job by its name."""
    with sqlite3.connect(EXPORTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, status FROM exports WHERE name = ?",
            (name,),
        )
        return cursor.fetchone()


def archive_export(filename: str) -> Path:
    """Compress a finished export file."""
    target = (EXPORTS_DIR / filename).resolve()
    if target.parent != EXPORTS_DIR.resolve() or not target.is_file():
        raise ValueError(f"Invalid export filename: {filename}")
    archive = target.with_suffix(f"{target.suffix}.gz")
    with target.open("rb") as source, gzip.open(archive, "wb") as destination:
        shutil.copyfileobj(source, destination)
    target.unlink()
    return archive


def generate_download_token() -> str:
    """Create a token for one-time download links."""
    return secrets.token_urlsafe(DOWNLOAD_TOKEN_BYTES)


def build_share_email(recipient: str, link: str) -> str:
    """Render the share notification email body."""
    if urlparse(link).scheme not in ALLOWED_LINK_SCHEMES:
        raise ValueError(f"Unsupported download link scheme: {link}")
    return (
        f"<p>Hello {escape(recipient)}, your export is ready: "
        f'<a href="{escape(link)}">download</a></p>'
    )
