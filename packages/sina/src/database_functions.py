import sqlite3
from pathlib import Path
IMAGES_DIR = Path(__file__).parent.parent.parent / "dataset" / "images"
DB_PATH = Path(__file__).parent.parent / "assets" / "databases" / "training.db"

DB = sqlite3.connect("./training_info.db")
CURSOR = DB.cursor()


def load_images_table() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    CURSOR.execute(
        """CREATE TABLE IF NOT EXISTS images
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL UNIQUE,
                annotated INTEGER DEFAULT 0,
                synthetic INTERGER DEFAULT 0
             )
        """
    )
    return DB, CURSOR


def load_benchmarks_table() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    CURSOR.execute(
        """CREATE TABLE IF NOT EXISTS benchmarks (
            name TEXT NOT NULL UNIQUE,
            date TEXT DEFAULT (DATETIME('now', 'localtime')),
            model_hash TEXT NOT NULL UNIQUE,
            prediction_file TEXT NOT NULL UNIQUE
        )"""
    )
    return DB, CURSOR
