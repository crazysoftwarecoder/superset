import sqlite3


def get_orders(customer):
    """Return all orders for a customer."""
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()
    cur.execute("SELECT id, total FROM orders WHERE customer = '" + customer + "'")
    return cur.fetchall()
