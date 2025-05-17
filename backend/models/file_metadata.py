import sqlite3

DB_PATH = "metadata.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            scene_type TEXT,
            destination TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
        )


def save_metadata(filename, scene_type, destination):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO metadata (filename, scene_type, destination) VALUES (?, ?, ?)",
            (filename, scene_type, destination),
        )
