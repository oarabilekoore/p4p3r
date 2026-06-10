# This file migrates images in the staging folder to the training folder
# to avoid duplicates by storing the file hashes and compares everytime
# it moves and destroys duplicates.

import shutil
import sqlite3
from pathlib import Path

import imagehash
from PIL import Image

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
    for image in images:
        with Image.open(image) as img:
            hash_value = imagehash.phash(img.convert("RGB"))
            image_hashes[image.name] = str(hash_value)
    return image_hashes


def load_db():
    img_db = sqlite3.connect("../dataset/dataset.db")
    cursor = img_db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL UNIQUE, hash TEXT NOT NULL UNIQUE)"
    )
    return img_db, cursor


def migrate_images(images: list[Path], image_hashes: dict[str, str], db_cursor):
    for image in images:
        hash_value = image_hashes[image.name]
        db_cursor.execute("SELECT 1 FROM images WHERE hash = ?", (hash_value,))
        already_exists = db_cursor.fetchone()

        if not already_exists:
            db_cursor.execute(
                "INSERT INTO images (filename, hash) VALUES (?, ?)",
                (image.name, hash_value),
            )
            shutil.move(image, training_folder / image.name)


check_paths()
img_db, cursor = load_db()
images_in_staging = get_images_in_staging()
image_hashes = get_image_hashes(images_in_staging)
migrate_images(images_in_staging, image_hashes, cursor)
img_db.commit()
img_db.close()
