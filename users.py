import sqlite3


def find_user(username):
    """Look up a user by username."""
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT id, email, role FROM users WHERE username = '" + username + "'")
    return cur.fetchone()
