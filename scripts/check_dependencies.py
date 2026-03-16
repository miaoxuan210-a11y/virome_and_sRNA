#!/usr/bin/env python3
"""Check required binaries and Python scripts for this repository."""
from __future__ import annotations

import shutil
import sys

REQUIRED_BINARIES = ["snakemake", "fastp", "bowtie2"]
OPTIONAL_BINARIES = ["spades.py", "Trinity", "blastn", "interproscan.sh"]


def check(names: list[str]) -> list[str]:
    missing = []
    for name in names:
        if shutil.which(name) is None:
            missing.append(name)
    return missing


def main() -> int:
    missing_required = check(REQUIRED_BINARIES)
    missing_optional = check(OPTIONAL_BINARIES)

    if missing_required:
        print("[ERROR] Missing required binaries for full Snakemake run:")
        for x in missing_required:
            print(f"  - {x}")
    else:
        print("[OK] Required binaries are available.")

    if missing_optional:
        print("[WARN] Optional/production binaries not found (expected for mock mode):")
        for x in missing_optional:
            print(f"  - {x}")

    return 1 if missing_required else 0


if __name__ == "__main__":
    raise SystemExit(main())
