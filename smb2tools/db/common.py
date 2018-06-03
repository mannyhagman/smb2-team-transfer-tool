import sqlite3

conn = None
cur = None

def setup():
    global conn, cur
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()

def teardown():
    global conn
    conn.commit()
    conn.close()

def get_cursor():
    return cur

def get_conn():
    return conn
