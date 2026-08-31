import sqlite3


def get_invoice(invoice_id):
    """Fetch an invoice by id."""
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute("SELECT id, amount, customer FROM invoices WHERE id = '" + invoice_id + "'")
    return cur.fetchone()
