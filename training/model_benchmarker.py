
import argparse
import hashlib
import sqlite3
import os
import shutil
from ultralytics import YOLO
import json
import time
import tkinter as tk
from tkinter import filedialog
from urllib.parse import unquote
from rich.console import Console
from rich.progress import track
from urllib.parse import unquote
from pathlib import Path

console = Console()

DATASET_IMAGES_DIR = Path("../dataset/images/training")
DATASET_LABELS_DIR = Path("../dataset/labels")
MODELS_DIR = Path("./models")
DB_PATH = Path("./training_info.db")

DEBUG = False


def check_paths():
    if not MODELS_DIR.exists() or not DATASET_LABELS_DIR.exists():
        raise FileNotFoundError(f"Models directory or Labels directory not found: {MODELS_DIR} / {DATASET_LABELS_DIR}")
    if not DATASET_IMAGES_DIR.exists():
        raise FileNotFoundError(f"Images directory not found: {DATASET_IMAGES_DIR}")


def load_db():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS benchmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            date TEXT DEFAULT (DATETIME('now', 'localtime')),
            model_hash TEXT NOT NULL UNIQUE,
            prediction_file TEXT NOT NULL UNIQUE
        )"""
    )
    try:
        cursor.execute(
            "ALTER TABLE images ADD COLUMN annotated INTEGER DEFAULT 0"
        )
    except sqlite3.OperationalError:
        pass
    db.commit()
    return db, cursor


def reset_benchmarks_table():
    """Drop and recreate benchmarks table. Debug only."""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS benchmarks")
    db.commit()
    db.close()
    console.print("[yellow][DEBUG] Benchmarks table dropped and will be recreated.[/yellow]")


def hash_model_file(model_path: str) -> str:
    hasher = hashlib.sha256()
    with open(model_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def debug_override_existing_hash(cursor, db, model_hash: str):
    """Delete existing benchmark entry for this hash so it can be re-run. Debug only."""
    cursor.execute(
        "SELECT name, prediction_file FROM benchmarks WHERE model_hash = ?",
        (model_hash,)
    )
    row = cursor.fetchone()
    if row:
        name, prediction_file = row
        console.print(f"[yellow][DEBUG] Existing benchmark '{name}' found — deleting entry.[/yellow]")
        cursor.execute("DELETE FROM benchmarks WHERE model_hash = ?", (model_hash,))
        old_file = Path(prediction_file)
        if old_file.exists():
            old_file.unlink()
            console.print(f"[yellow][DEBUG] Deleted old prediction file: {old_file}[/yellow]")
        db.commit()


def is_model_already_benchmarked(cursor, model_hash: str) -> bool:
    cursor.execute(
        "SELECT name FROM benchmarks WHERE model_hash = ?", (model_hash,)
    )
    row = cursor.fetchone()
    if row:
        console.print(f"[red]✗[/red] Model already benchmarked under the name: '[cyan]{row[0]}[/cyan]'")
        return True
    return False


def get_images_not_annotated_and_mark_annotated_images() -> list[str]:
    db, cursor = load_db()
    images_not_annotated = []
    annotated_images = []

    for f in track(list(DATASET_LABELS_DIR.iterdir()), description="Reading label files..."):
        if not f.is_file():
            continue
        with open(f, "r") as file:
            data = json.load(file)
        filename = Path(unquote(data["task"]["data"]["image"].split("?d=")[1])).name
        annotated_images.append(filename)
        cursor.execute(
            "UPDATE images SET annotated = 1 WHERE filename = ?",
            (filename,)
        )

    db.commit()
    console.print(f"[green]✓[/green] Marked [cyan]{len(annotated_images)}[/cyan] images as annotated.")

    for f in DATASET_IMAGES_DIR.iterdir():
        if not f.is_file():
            continue
        if f.name not in annotated_images:
            images_not_annotated.append(f.name)

    db.close()
    console.print(f"[green]✓[/green] Found [cyan]{len(images_not_annotated)}[/cyan] unannotated images.")
    return images_not_annotated


def move_images_not_annotated_to_special_dir(imagesList: list[str]) -> Path:
    test_dir = MODELS_DIR / "test_images"
    test_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for filename in track(imagesList, description="Copying test images..."):
        src = DATASET_IMAGES_DIR / filename
        if src.exists():
            shutil.copy(str(src), test_dir / filename)
            copied += 1
        else:
            console.print(f"[yellow]Warning:[/yellow] {filename} not found, skipping.")
    console.print(f"[green]✓[/green] Copied [cyan]{copied}[/cyan] images to test directory.")
    return test_dir


def select_model_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select YOLO Model",
        filetypes=[("PyTorch Model", "*.pt")]
    )
    return file_path


def commit_model_details_to_db(cursor, db, name, model_hash, prediction):
    cursor.execute(
        "INSERT INTO benchmarks (name, model_hash, prediction_file) VALUES (?,?,?)",
        (name, model_hash, str(prediction))
    )
    db.commit()


def benchmark_model(model_name: str | None, model_path: str | None):
    if DEBUG:
        reset_benchmarks_table()

    check_paths()
    db, cursor = load_db()

    console.print("[bold]Model Benchmarker[/bold]")

    if not model_name:
        model_name = console.input("[cyan]Enter the name of the model:[/cyan] ").strip()

    if not model_path:
        console.print("[cyan]A dialog will open — select the .pt model file.[/cyan]")
        time.sleep(2)
        model_path = select_model_file()

    if not model_path:
        console.print("[red]✗[/red] No file selected, exiting.")
        db.close()
        return

    console.print(f"[green]✓[/green] Model file selected: [cyan]{model_path}[/cyan]")

    model_hash = hash_model_file(model_path)

    if DEBUG:
        debug_override_existing_hash(cursor, db, model_hash)
    elif is_model_already_benchmarked(cursor, model_hash):
        db.close()
        return

    images_not_annotated = get_images_not_annotated_and_mark_annotated_images()

    if not images_not_annotated:
        console.print("[yellow]No unannotated images found, exiting.[/yellow]")
        db.close()
        return

    img_dir = move_images_not_annotated_to_special_dir(images_not_annotated)

    model = YOLO(model_path)
    labelled_dir = MODELS_DIR / f"{model_name}_labelled"
    labelled_dir.mkdir(parents=True, exist_ok=True)
    prediction_file = MODELS_DIR / f"{model_name}.jsonl"

    console.print(f"[cyan]Running model against {len(images_not_annotated)} images...[/cyan]")
    results = model.predict(
        source=str(img_dir),
        conf=0.25,
        save=True,
        project=str(MODELS_DIR),
        name=f"{model_name}_labelled",
        exist_ok=True
    )

    with open(prediction_file, "w") as pf:
        for r in results:
            image_filename = Path(r.path).name
            boxes = []
            if r.boxes is not None:
                boxes = [
                    {
                        "class_id": int(box.cls),
                        "class_name": model.names[int(box.cls)],
                        "confidence": float(box.conf),
                        "xyxy": box.xyxy.tolist()
                    }
                    for box in r.boxes
                ]
            pf.write(json.dumps({"image": image_filename, "boxes": boxes}) + "\n")

    commit_model_details_to_db(cursor, db, model_name, model_hash, prediction_file)
    console.print(f"[green]✓[/green] Benchmark complete.")
    console.print(f"[green]✓[/green] Predictions saved to [cyan]{prediction_file}[/cyan]")
    console.print(f"[green]✓[/green] Labelled images saved to [cyan]{labelled_dir}[/cyan]")
    db.close()


def main():
    parser = argparse.ArgumentParser(description="Benchmark a YOLO model against unannotated images.")
    parser.add_argument("--name", type=str, help="Name for this benchmark run", default=None)
    parser.add_argument("--model", type=str, help="Path to the .pt model file", default=None)
    args = parser.parse_args()
    benchmark_model(args.name, args.model)


main()
