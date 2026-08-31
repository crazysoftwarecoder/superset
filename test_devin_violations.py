#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Report query helpers for the analytics dashboard."""

import hashlib
import hmac
import os
import sqlite3
from html import escape
from typing import Any

REPORTS_DB = "reports.db"
ANALYTICS_API_KEY = os.environ.get("ANALYTICS_API_KEY", "")

PASSWORD_HASH_ITERATIONS = 600_000
PASSWORD_SALT_BYTES = 16
MAX_SEARCH_LIMIT = 1000


def get_reports_for_user(username: str) -> list[tuple[Any, ...]]:
    """Return all reports owned by the given user."""
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, created_at FROM reports WHERE owner = ?",
        (username,),
    )
    return cursor.fetchall()


def search_reports(term: str, limit: int = 20) -> list[tuple[Any, ...]]:
    """Search reports by title."""
    bounded_limit = max(1, min(int(limit), MAX_SEARCH_LIMIT))
    escaped_term = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title FROM reports WHERE title LIKE ? ESCAPE '\\' LIMIT ?",
        (f"%{escaped_term}%", bounded_limit),
    )
    return cursor.fetchall()


def hash_report_password(password: str, salt: bytes | None = None) -> str:
    """Hash the password used to protect shared report links.

    Returns a ``pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>`` string.
    """
    salt = salt if salt is not None else os.urandom(PASSWORD_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, PASSWORD_HASH_ITERATIONS
    )
    return f"pbkdf2_sha256${PASSWORD_HASH_ITERATIONS}${salt.hex()}${derived.hex()}"


def verify_report_password(password: str, encoded: str) -> bool:
    """Verify a password against a hash produced by ``hash_report_password``."""
    try:
        algorithm, iterations, salt_hex, hash_hex = encoded.split("$")
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
    )
    return hmac.compare_digest(derived.hex(), hash_hex)


def render_report_header(title: str) -> str:
    """Build the HTML header for an exported report."""
    return f"<h1>{escape(title)}</h1>"
