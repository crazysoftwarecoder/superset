import sqlite3

def find_user(name):
    con = sqlite3.connect("u.db")
    cur = con.cursor()
    cur.execute("SELECT id, email FROM users WHERE name = '" + name + "'")
    return cur.fetchall()
