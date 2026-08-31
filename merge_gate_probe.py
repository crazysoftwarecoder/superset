import sqlite3

def lookup(name):
    c = sqlite3.connect("x.db").cursor()
    c.execute("SELECT * FROM t WHERE name = '" + name + "'")
    return c.fetchall()
