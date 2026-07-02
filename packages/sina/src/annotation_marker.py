import sqlite3
import json
from pathlib import Path
from urllib.parse import unquote
from rich.console import Console

console = Console()

DATASET_LABELS_DIR = Path("../dataset/labels")

DB_PATH = Path("./training_info.db")


def check_paths():
    if not DATASET_LABELS_DIR.exists():
        raise FileNotFoundError(f"Labels directory not found: {
                                DATASET_LABELS_DIR}")


def load_db():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    return db, cursor


def mark_annotated_images():
    check_paths()
    db, cursor = load_db()

    annotated = []
    skipped = 0

    label_files = [f for f in DATASET_LABELS_DIR.iterdir() if f.is_file()]

    for f in label_files:
        try:
            with open(f, "r") as file:
                data = json.load(file)
            filename = Path(
                unquote(data["task"]["data"]["image"].split("?d=")[1])).name
            cursor.execute(
                "UPDATE images SET annotated = 1 WHERE filename = ?",
                (filename,)
            )
            annotated.append(filename)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            console.print(
                f"[yellow]Warning:[/yellow] Could not parse {f.name} — {e}")
            skipped += 1

    db.commit()
    db.close()

    console.print(
        f"[green]✓[/green] Marked [cyan]{len(annotated)}[/cyan] images as annotated.")
    if skipped:
        console.print(f"[yellow]Skipped {
                      skipped} label files due to errors.[/yellow]")


mark_annotated_images()
