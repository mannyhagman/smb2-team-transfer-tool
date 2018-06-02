import sqlite3

conn = None
cur = None

def setup():
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()

def teardown():
    conn.close()
