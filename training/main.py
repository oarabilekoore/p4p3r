"""vibes used in this file too :( -- mb, claude sonnet 4.6"""
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

SRC = Path(__file__).parent / "src"

COMMANDS = {
    "scan":     ("document_scanner.py",  "Batch scan pages from the MG2540"),
    "migrate":  ("dataset_migrator.py",  "Move staged images → training, dedup by hash"),
    "annotate": ("annotation_marker.py", "Sync Label Studio annotations → DB"),
    "bench":    ("model_benchmarker.py", "Benchmark a .pt model on unannotated images"),
    "train":    ("model_trainer.py",     "Convert labels + train YOLO11 (Colab script)"),
    "synth":    ("synthetic_data.py",    "Generate synthetic page images for training"),
}


def print_header():
    console.print(Panel(
        Text.assemble(
            ("p4p3r", "bold white"),
            ("  training pipeline\n", "dim white"),
            ("Handwritten document understanding — YOLO11 + ONNX", "italic cyan"),
        ),
        border_style="bright_blue",
        padding=(0, 2),
    ))


def print_help():
    table = Table(box=box.SIMPLE, show_header=True,
                  header_style="bold cyan", padding=(0, 2))
    table.add_column("command", style="bold white", no_wrap=True)
    table.add_column("description", style="dim white")

    for cmd, (_, desc) in COMMANDS.items():
        table.add_row(cmd, desc)

    table.add_row("help", "Show this message")
    table.add_row("exit", "Quit")

    console.print(table)


def run_module(script: str, extra_args: list[str]):
    path = SRC / script
    if not path.exists():
        console.print(f"[red]✗[/red] Script not found: [white]{path}[/white]")
        return
    result = subprocess.run([sys.executable, str(path)] + extra_args)
    if result.returncode != 0:
        console.print(f"[red]✗[/red] Exited with code {result.returncode}")


def repl():
    print_header()
    print_help()

    while True:
        try:
            raw = console.input(
                "\n[bold bright_blue]paper[/bold bright_blue][dim]>[/dim] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]bye[/dim]")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]

        if cmd in ("exit", "quit", "q"):
            console.print("[dim]bye[/dim]")
            break
        elif cmd in ("help", "h", "?"):
            print_help()
        elif cmd in COMMANDS:
            script, _ = COMMANDS[cmd]
            run_module(script, args)
        else:
            console.print(f"[yellow]Unknown command:[/yellow] [white]{
                          cmd}[/white]  — type [cyan]help[/cyan] to list commands")


repl()
