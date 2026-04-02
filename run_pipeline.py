"""Run full pipeline: Excel -> SQLite -> Power BI CSV export."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PY = sys.executable


def run(name: str) -> None:
    path = SCRIPTS / name
    print(f"\n=== {name} ===\n")
    subprocess.run([PY, str(path)], check=True)


def main() -> None:
    run("01_generate_excel_data.py")
    run("02_etl_sqlite.py")
    run("03_export_for_powerbi.py")
    print("\nPipeline complete. Optional: python scripts/04_python_analysis.py")


if __name__ == "__main__":
    main()
