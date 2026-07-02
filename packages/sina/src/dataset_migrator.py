import shutil
from pathlib import Path

import imagehash
from PIL import Image
from rich.console import Console
from rich.progress import track
from src.database_functions import load_images_table
console = Console()


accepted_image_file_formats = [".jpg", ".jpeg", ".png", ".webp"]


def get_image_hashes(images: list[Path]) -> dict[str, str]:
    image_hashes = {}
    for image in track(images, description="Hashing images..."):
        with Image.open(image) as img:
            hash_value = imagehash.phash(img.convert("RGB"))
            image_hashes[image.name] = str(hash_value)
    return image_hashes


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


console.print("[bold]Dataset Migrator[/bold]")
img_db, cursor = load_images_table()
