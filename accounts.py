import sqlite3


def find_account(email):
    """Look up an account by email address."""
    conn = sqlite3.connect("accounts.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, balance FROM accounts WHERE email = ?",
        (email,),
    )
    return cur.fetchone()
