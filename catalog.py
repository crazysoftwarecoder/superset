import sqlite3
from contextlib import closing
from typing import Any, Optional


def find_product(sku: str) -> Optional[tuple[Any, ...]]:
    """Look up a product by SKU."""
    with closing(sqlite3.connect("catalog.db")) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, price FROM products WHERE sku = ?",
            (sku,),
        )
        return cur.fetchone()
