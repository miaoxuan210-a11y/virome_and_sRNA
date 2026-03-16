#!/usr/bin/env python3
"""Minimal placeholder sRNA analysis script for workflow scaffolding."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Placeholder sRNA analysis")
    parser.add_argument("--input", required=True, help="Host-removed FASTQ file")
    parser.add_argument("--reference", required=True, help="sRNA reference file")
    parser.add_argument("--annotation", required=True, help="Output annotation TSV")
    parser.add_argument("--length-dist", required=True, help="Output length distribution TSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    Path(args.annotation).parent.mkdir(parents=True, exist_ok=True)

    with open(args.annotation, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["feature", "count"])
        writer.writerow(["rRNA", 0])
        writer.writerow(["tRNA", 0])
        writer.writerow(["miRNA", 0])
        writer.writerow(["snRNA", 0])
        writer.writerow(["snoRNA", 0])

    with open(args.length_dist, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["length", "count"])
        for length in range(18, 31):
            writer.writerow([length, 0])


if __name__ == "__main__":
    main()
