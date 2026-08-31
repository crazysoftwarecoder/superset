import sqlite3
from typing import Any, Optional


def find_account(email: str) -> Optional[tuple[Any, ...]]:
    """Look up an account by email address."""
    conn = sqlite3.connect("accounts.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, balance FROM accounts WHERE email = ?",
        (email,),
    )
    return cur.fetchone()
