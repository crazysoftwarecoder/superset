import sqlite3


def find_order(code):
    """Look up an order by code."""
    with sqlite3.connect("shop.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, total FROM orders WHERE code = ?", (code,))
        return cur.fetchone()
