# This file migrates images in the staging folder to the training folder
# to avoid duplicates by storing the file hashes and compares everytime
# it moves and destroys duplicates.

import shutil
import sqlite3
from pathlib import Path

import imagehash
from PIL import Image
from rich.console import Console
from rich.progress import track

console = Console()

accepted_image_file_formats = [".jpg", ".jpeg", ".png", ".webp"]
training_folder = Path("../dataset/images/training")
staging_folder = Path("../dataset/images/staging")


def check_paths():
    if not training_folder.exists() or not staging_folder.exists():
        raise FileNotFoundError(
            f"Training folder or Staging folder not found: {
                training_folder} / {staging_folder}"
        )


def get_images_in_staging() -> list[Path]:
    images_in_staging = []
    for f in staging_folder.glob("*"):
        if f.suffix in accepted_image_file_formats:
            images_in_staging.append(f)
    return images_in_staging


def get_image_hashes(images: list[Path]) -> dict[str, str]:
    image_hashes = {}
    for image in track(images, description="Hashing images..."):
        with Image.open(image) as img:
            hash_value = imagehash.phash(img.convert("RGB"))
            image_hashes[image.name] = str(hash_value)
    return image_hashes


def load_db():
    img_db = sqlite3.connect("./training_info.db")
    cursor = img_db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS images
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL UNIQUE,
                annotated INTEGER DEFAULT 0
             )
        """
    )
    return img_db, cursor


def migrate_images(images: list[Path], image_hashes: dict[str, str], db_cursor):
    moved = 0
    skipped = 0
    for image in track(images, description="Migrating images..."):
        hash_value = image_hashes[image.name]
        db_cursor.execute("SELECT 1 FROM images WHERE hash = ?", (hash_value,))
        already_exists = db_cursor.fetchone()
        if not already_exists:
            db_cursor.execute(
                "INSERT INTO images (filename, hash) VALUES (?, ?)",
                (image.name, hash_value),
            )
            shutil.move(image, training_folder / image.name)
            moved += 1
        else:
            skipped += 1
    return moved, skipped


check_paths()
console.print("[bold]Dataset Migrator[/bold]")
img_db, cursor = load_db()
images_in_staging = get_images_in_staging()

if not images_in_staging:
    console.print("[yellow]No images found in staging folder.[/yellow]")
else:
    console.print(
        f"Found [cyan]{len(images_in_staging)}[/cyan] images in staging.")
    image_hashes = get_image_hashes(images_in_staging)
    moved, skipped = migrate_images(images_in_staging, image_hashes, cursor)
    img_db.commit()
    console.print(f"[green]✓[/green] Moved [cyan]{
                  moved}[/cyan] images. Skipped [cyan]{skipped}[/cyan] duplicates.")

img_db.close()
