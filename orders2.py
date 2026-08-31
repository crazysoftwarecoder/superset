import sqlite3


def find_order(code):
    """Look up an order by code."""
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT id, total FROM orders WHERE code = '" + code + "'")
    return cur.fetchone()
