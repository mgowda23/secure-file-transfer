# db.py
import sqlite3, datetime

DB_FILE = "transfers.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filesize INTEGER,
            timestamp TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_transfer(filename, filesize, status):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transfers (filename, filesize, timestamp, status) VALUES (?, ?, ?, ?)",
        (filename, filesize, datetime.datetime.now().isoformat(), status)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

