""" vibes were used in this file. beware :) -- claude sonnet 4.6"""


import sqlite3
import subprocess
import sys
import termios
import threading
import tty
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

SCANNER_DEVICE = "pixma:04A9176D_AB9FA5"
RESOLUTION = 300
OUTPUT_DIR = Path(__file__).parent.parent.parent / "dataset" / "images"
DB_PATH = Path(__file__).parent.parent / "assets" / "databases" / "training.db"
DEFAULT_DELAY = 20


def setup_db():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            filename  TEXT NOT NULL UNIQUE,
            hash      TEXT NOT NULL UNIQUE,
            annotated INTEGER DEFAULT 0
        )
    """)
    db.commit()
    return db, cur


def register_image(cur, filename: str):
    cur.execute(
        "INSERT OR IGNORE INTO images (filename, hash) VALUES (?, ?)",
        (filename, filename),
    )


def scan_image() -> Path:
    timestamp = datetime.now().strftime("%d-%m-%y_%H:%M")
    filename = f"scanned-{timestamp}.png"
    output_path = OUTPUT_DIR / filename

    console.print(
        f"\n[bold cyan]▶ Scanning →[/bold cyan] [white]{filename}[/white]")
    result = subprocess.run(
        [
            "scanimage",
            "-d", SCANNER_DEVICE,
            "--resolution", str(RESOLUTION),
            "--mode", "Color",
            "--format=png",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        console.print(
            f"[bold red]✗ Scan failed:[/bold red] {result.stderr.decode().strip()}")
        return None

    output_path.write_bytes(result.stdout)
    console.print(
        f"[bold green]✓ Saved[/bold green] [white]{output_path}[/white]")
    return output_path


def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def countdown(seconds: int) -> str:
    """Returns 's' (scan now), 'd' (delay), or None (timed out)."""
    pressed = [None]
    done = threading.Event()

    def listen():
        ch = getch()
        if ch in ("s", "d", "q"):
            pressed[0] = ch
            done.set()

    t = threading.Thread(target=listen, daemon=True)
    t.start()

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

    db, cur = setup_db()
    input()

    scan_count = 0
    delay = DEFAULT_DELAY

    while True:
        path = scan_image()
        if path:
            register_image(cur, path.name)
            db.commit()
            scan_count += 1
            console.print(f"  [dim]Total scanned: {scan_count}[/dim]")

        console.print(f"\n[bold]Next scan in {
                      delay}s.[/bold] Swap the page now.\n")
        key = countdown(delay)

        if key == "q":
            console.print("\n[bold yellow]Stopped.[/bold yellow]")
            break
        elif key == "d":
            delay += 15
            console.print(
                f"\n[cyan]+15s → now {delay}s delay.[/cyan] Swap the page.\n")
            key2 = countdown(delay)
            if key2 == "q":
                console.print("\n[bold yellow]Stopped.[/bold yellow]")
                break
        elif key == "s":
            console.print("\n[green]Scanning early…[/green]")

    db.close()
    console.print(f"\n[bold green]Done.[/bold green] {
                  scan_count} image(s) saved to [white]{OUTPUT_DIR}[/white]")


begin_scan()
