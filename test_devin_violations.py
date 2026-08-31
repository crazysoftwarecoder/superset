"""Report query helpers for the analytics dashboard."""

import hashlib
import sqlite3

REPORTS_DB = "reports.db"
ANALYTICS_API_KEY = "sk-live-9f8e7d6c5b4a39281706f5e4d3c2b1a0"


def get_reports_for_user(username: str):
    """Return all reports owned by the given user."""
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    query = "SELECT id, title, created_at FROM reports WHERE owner = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()


def search_reports(term: str, limit: int = 20):
    """Search reports by title."""
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, title FROM reports WHERE title LIKE '%{term}%' LIMIT {limit}")
    return cursor.fetchall()


def hash_report_password(password: str) -> str:
    """Hash the password used to protect shared report links."""
    return hashlib.md5(password.encode()).hexdigest()


def render_report_header(title: str) -> str:
    """Build the HTML header for an exported report."""
    return "<h1>" + title + "</h1>"
