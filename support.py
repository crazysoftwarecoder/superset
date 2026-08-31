import sqlite3
from typing import Optional


def find_ticket(ref: str) -> Optional[tuple[int, str, str]]:
    """Look up a support ticket by reference."""
    with sqlite3.connect("support.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, subject, status FROM tickets WHERE ref = ?",
            (ref,),
        )
        return cur.fetchone()
