import sqlite3

conn = sqlite3.connect("assistant.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    time TEXT
)
""")

conn.commit()


def add_task(text: str, time: str):
    cursor.execute(
        "INSERT INTO tasks (text, time) VALUES (?, ?)",
        (text, time)
    )
    conn.commit()
