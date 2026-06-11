import sys
import subprocess
from pathlib import Path

SCRIPTS = {
    "benchmark": Path("./model_benchmarker.py"),
    "migrate": Path("./dataset_migrator.py"),
    "annotate": Path("./annotation_marker.py"),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SCRIPTS:
        print("Usage: trainer <command>")
        print(f"Commands: {', '.join(SCRIPTS.keys())}")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]
    script = SCRIPTS[command]

    if not script.exists():
        print(f"Script not found: {script}")
        sys.exit(1)

    subprocess.run(["uv", "run", str(script), *args])


main()
