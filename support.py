import sqlite3


def find_ticket(ref):
    """Look up a support ticket by reference."""
    conn = sqlite3.connect("support.db")
    cur = conn.cursor()
    cur.execute("SELECT id, subject, status FROM tickets WHERE ref = '" + ref + "'")
    return cur.fetchone()
