import sqlite3
from pathlib import Path
from config import DB_PATH


Path(DB_PATH).touch(exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db() -> None:
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        date_published TEXT,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        is_sent INTEGER DEFAULT 0
    )
    """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT DEFAULT NULL,
        mailings INTEGER DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()

def add_news(title: str, link: str, date:str) -> None:
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO news (title, link, date_published) VALUES (?, ?, ?)", (title, link, date))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def add_user(id: int, username: str) -> None:
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (id, username))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_mailings_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, mailings FROM users WHERE mailings = 1")
    result = c.fetchall()
    conn.close()
    return result

def get_unsent_news():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
SELECT id, title, link, date_published 
FROM news 
WHERE is_sent = 0 
  AND date_published >= datetime('now', '-3 days')
ORDER BY date_published ASC
""")
    result = c.fetchall()
    conn.close()
    return result

def update_sent_news(id: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE news SET is_sent = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_subscribe_user(id:int, mailings: bool):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET mailings = ? WHERE id = ?", (1 if mailings else 0, id,))
    conn.commit()
    conn.close()

