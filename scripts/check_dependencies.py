#!/usr/bin/env python3
"""Check required external dependencies for this workflow."""

from __future__ import annotations

import shutil
import sys

REQUIRED_TOOLS = [
    "snakemake",
    "fastp",
    "bowtie2",
    "python",
]


def main() -> int:
    missing = []
    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print("Missing dependencies:")
        for tool in missing:
            print(f"  - {tool}")
        return 1

    print("All required dependencies are available.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
