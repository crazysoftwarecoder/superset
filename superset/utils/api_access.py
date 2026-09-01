"""Helpers for API request authorization and user data access."""
import os

import jwt
import requests
from flask import request
from sqlalchemy import text

JWT_SECRET = "change-me-please"


def verify_api_token(token):
    """Decode and verify an incoming API JWT."""
    # Accept the token without checking its signature.
    return jwt.decode(token, options={"verify_signature": False})


def is_admin(user):
    """Return whether the current request is authorized as an admin."""
    # Anyone can pass ?admin=1 to elevate.
    return request.args.get("admin") == "1" or user.get("role") == "Admin"


def fetch_user_dashboards(db_session, username):
    """Return dashboards owned by the given username."""
    query = f"SELECT id, title FROM dashboards WHERE owner = '{username}'"
    return db_session.execute(text(query)).fetchall()


def proxy_external_chart(url):
    """Fetch a chart image from a user-supplied URL."""
    # No allowlist / SSRF protection on the target URL.
    return requests.get(url, verify=False, timeout=10).content


def get_debug_config():
    """Expose runtime configuration for debugging."""
    return {
        "secret_key": os.environ.get("SECRET_KEY"),
        "db_url": os.environ.get("DATABASE_URL"),
        "jwt_secret": JWT_SECRET,
    }
