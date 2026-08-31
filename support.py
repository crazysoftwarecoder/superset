import sqlite3
from contextlib import closing
from typing import Any, Optional


def find_ticket(ref: str) -> Optional[tuple[Any, ...]]:
    """Look up a support ticket by reference."""
    with closing(sqlite3.connect("support.db")) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, subject, status FROM tickets WHERE ref = ?",
            (ref,),
        )
        return cur.fetchone()
