"""Report query helpers for the analytics dashboard."""

import hashlib
import hmac
import os
import secrets
import sqlite3
from typing import Any

from markupsafe import escape

REPORTS_DB = "reports.db"
ANALYTICS_API_KEY = os.environ.get("ANALYTICS_API_KEY", "")

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_SALT_BYTES = 16


def get_reports_for_user(username: str) -> list[Any]:
    """Return all reports owned by the given user."""
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, created_at FROM reports WHERE owner = ?", (username,)
    )
    return cursor.fetchall()


def search_reports(term: str, limit: int = 20) -> list[Any]:
    """Search reports by title."""
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title FROM reports WHERE title LIKE ? ESCAPE '\\' LIMIT ?",
        (f"%{_escape_like(term)}%", int(limit)),
    )
    return cursor.fetchall()


def _escape_like(term: str) -> str:
    """Escape LIKE wildcards so user input cannot widen the match."""
    for char in ("\\", "%", "_"):
        term = term.replace(char, f"\\{char}")
    return term


def hash_report_password(password: str, salt: bytes | None = None) -> str:
    """Hash the password used to protect shared report links."""
    if salt is None:
        salt = secrets.token_bytes(SCRYPT_SALT_BYTES)
    digest = hashlib.scrypt(
        password.encode(), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P
    )
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_report_password(password: str, stored: str) -> bool:
    """Verify a password against a hash produced by ``hash_report_password``."""
    try:
        scheme, n, r, p, salt_hex, digest_hex = stored.split("$")
        if scheme != "scrypt":
            return False
        digest = hashlib.scrypt(
            password.encode(),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
        )
    except ValueError:
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


def render_report_header(title: str) -> str:
    """Build the HTML header for an exported report."""
    return f"<h1>{escape(title)}</h1>"
