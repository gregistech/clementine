import sqlite3
from sqlite3 import Error
def create_connection(db):
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    finally:
        return conn
conn = create_connection("asd.db")
cur = conn.cursor()
print(conn, cur)
cur.execute("INSERT INTO tags (name, content) VALUES (?, ?)", ("lol d d", "asd asda dad sad asd a"))
