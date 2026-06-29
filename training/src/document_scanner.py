import subprocess
import sys
import termios
import threading
import tty
from datetime import datetime
from pathlib import Path
from typing import List

import imagehash
from PIL import Image
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.database_functions import load_images_table, DB_PATH, IMAGES_DIR

console = Console()

RESOLUTION = 75
SCAN_LIMIT = 30  # Prnter gets hot
DEFAULT_DELAY = 29

# Dynamic state variable populated at runtime
scanner_device_path = None


class ScannerDeviceNotFound(Exception):
    pass


def find_scanner() -> str:
    """Queries SANE backend to locate and isolate the first valid scanner address string."""
    console.print("[dim] Searching for scanner devices.")
    result = subprocess.run(
        ["scanimage", "-f", "%d"],
        capture_output=True,
        text=True,
        check=True
    )
    device = result.stdout.strip()
    if device:
        first_machine = device.split("\n")[0]
        console.print("[bold green] Found SANE scanner")
        console.print(f"[white] Device name: {first_machine}")
        return first_machine
    else:
        raise ScannerDeviceNotFound("No scanning device was found")


def register_image(cur, filename: str):
    hashval: str = None
    try:
        with Image.open(IMAGES_DIR / filename) as img:
            hashval = str(imagehash.phash(img.convert("RGB")))

        cur.execute(
            "INSERT OR IGNORE INTO images (filename, hash) VALUES (?, ?)",
            (filename, hashval),
        )
    except Exception as e:
        console.print(f"[bold red] Failed to parse phash for {
                      filename}: {e}[/bold red]")


def delete_last_scan(cur, db, path: Path):
    if path and path.exists():
        try:
            path.unlink()
            cur.execute("DELETE FROM images WHERE filename = ?", (path.name,))
            db.commit()

            console.print(
                "[bold red] Deleted last scan from disk and database.[/bold red]")
        except Exception as e:
            console.print(
                f"[bold red] Error trying to delete last scan: {e}[/bold red]")
    else:
        console.print(
            "[yellow] No valid recent scan file found to delete.[/yellow]")


def scan_image() -> Path:
    global scanner_device_path
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    filename = f"scanned-{timestamp}.png"
    output_path = IMAGES_DIR / filename

    console.print(
        f"\n[bold cyan] Scanning ->[/bold cyan] [white]{filename}[/white]")
    result = subprocess.run(
        [
            "scanimage",
            "-d", scanner_device_path,
            "--resolution", str(RESOLUTION),
            "--mode", "Color",
            "--format=png",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        console.print(
            f"[bold red] Scan failed:[/bold red] {result.stderr.decode().strip()}")
        return None

    output_path.write_bytes(result.stdout)
    console.print(
        f"[bold green] Saved[/bold green] [white]{output_path}[/white]")
    return output_path


def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def start_listener(events: List, done_event):
    def listen():
        while not done_event.is_set():
            ch = getch()
            if ch in ("a", "s", "d", "q"):
                events[0] = ch
                done_event.set()
                break
    t = threading.Thread(target=listen, daemon=True)
    t.start()


def countdown(seconds: int) -> str:
    pressed = [None]
    done = threading.Event()

    start_listener(pressed, done)

    for remaining in range(seconds, 0, -1):
        if done.is_set():
            break
        bar_filled = int((seconds - remaining) / seconds * 20)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        color = "green" if remaining > 10 else "yellow" if remaining > 5 else "red"
        console.print(
            f"  [{color}]{bar}[/{color}] [bold]{remaining:>2}s[/bold]  "
            f"[dim]s[/dim]=scan now  [dim]d[/dim]=more time  [dim]q[/dim]=quit",
            end="\r",
        )
        done.wait(timeout=1)

    console.print(" " * 70, end="\r")
    return pressed[0]


def begin_scan():
    global scanner_device_path

    console.print(Panel(
        Text.assemble(
            ("p4p3r Batch Scanner\n", "bold white"),
            ("Place a page face-down on the glass, then press ", "dim"),
            ("Enter", "bold cyan"),
            (" to begin.", "dim"),
        ),
        border_style="cyan",
        padding=(0, 2),
    ))

    try:
        scanner_device_path = find_scanner()
    except ScannerDeviceNotFound as e:
        console.print(
            f"[bold red]Hardware Initialization Error: {e}[/bold red]")
        return

    db, cur = load_images_table()
    input()

    scan_count = 0
    delay = DEFAULT_DELAY
    last_path = None
    should_stop = False

    while not should_stop:
        path = scan_image()
        if path:
            last_path = path
            register_image(cur, path.name)
            db.commit()
            scan_count += 1
            console.print(f"  [dim]Total scanned: {
                          scan_count}/{SCAN_LIMIT}[/dim]")

        # Automatically stop if the configured limit is reached
        if scan_count >= SCAN_LIMIT:
            console.print(f"\n[bold yellow] Scan limit of {
                          SCAN_LIMIT} reached. Stopping batch.[/bold yellow]")
            should_stop = True
            continue

        console.print(f"\n[bold]Next scan in {
                      delay}s.[/bold] Swap the page now.\n")
        key = countdown(delay)

        match key:
            case "a":
                delete_last_scan(cur, db, last_path)
                if scan_count > 0:
                    scan_count -= 1
                delay = DEFAULT_DELAY

            case "s":
                delay = 0
                console.print("\n[green]Scanning early...[/green]")

            case "d":
                delay += 15
                console.print(
                    f"\n[cyan]+15s -> now {delay}s delay.[/cyan] Swap the page.\n")
                key2 = countdown(delay)
                if key2 == "q":
                    console.print("\n[bold yellow]Stopped.[/bold yellow]")
                    should_stop = True
                elif key2 == "s":
                    delay = 0
                    console.print("\n[green]Scanning early...[/green]")
                else:
                    delay = DEFAULT_DELAY

            case "q":
                console.print("\n[bold yellow]Stopped.[/bold yellow]")
                should_stop = True

            case _:
                delay = DEFAULT_DELAY

    db.close()
    console.print(f"\n[bold green]Done.[/bold green] {
                  scan_count} image(s) saved to [white]{IMAGES_DIR}[/white]")


begin_scan()
