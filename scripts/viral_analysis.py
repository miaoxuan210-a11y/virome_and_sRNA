#!/usr/bin/env python3
"""Minimal placeholder viral analysis script for workflow scaffolding."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Placeholder viral analysis")
    parser.add_argument("--input", required=True, help="Host-removed FASTQ file")
    parser.add_argument("--reference", required=True, help="Viral reference FASTA")
    parser.add_argument("--contigs", required=True, help="Output contigs FASTA")
    parser.add_argument("--annotation", required=True, help="Output annotation TSV")
    parser.add_argument("--abundance", required=True, help="Output abundance TSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    Path(args.contigs).parent.mkdir(parents=True, exist_ok=True)

    with open(args.contigs, "w", encoding="utf-8") as handle:
        handle.write(">contig_1\n")
        handle.write("NNNNNNNNNN\n")

    with open(args.annotation, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["contig", "best_hit", "evalue"])
        writer.writerow(["contig_1", "NA", "NA"])

    with open(args.abundance, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["taxon", "reads"])
        writer.writerow(["unclassified", 0])


if __name__ == "__main__":
    main()
