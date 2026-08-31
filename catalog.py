import sqlite3


def find_product(sku):
    """Look up a product by SKU."""
    conn = sqlite3.connect("catalog.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products WHERE sku = '" + sku + "'")
    return cur.fetchone()
