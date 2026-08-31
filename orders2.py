import sqlite3
from contextlib import closing
from typing import Any, Optional


def find_order(code: str) -> Optional[tuple[Any, ...]]:
    """Look up an order by code."""
    with closing(sqlite3.connect("shop.db")) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, total FROM orders WHERE code = ?",
            (code,),
        )
        return cur.fetchone()
