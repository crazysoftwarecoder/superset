import sqlite3
from contextlib import closing
from typing import Any, Optional


def find_account(email: str) -> Optional[tuple[Any, ...]]:
    """Look up an account by email address."""
    with closing(sqlite3.connect("accounts.db")) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, balance FROM accounts WHERE email = ?",
            (email,),
        )
        return cur.fetchone()
